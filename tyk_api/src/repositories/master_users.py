import random
from loguru import logger

from tyk_api.src.api import (
    get_tyk_users_api,
    get_tyk_users_admin_api
)

from tyk_api.src.settings import settings
from tyk_api.src.models import TykUserModel
from .vanila_tyk import TykUsersRepository
from tyk_api.src.generators import TykUserGenerator


class TempSuperAdminCTX:
    """Async context manager for creating and cleaning up a temporary super admin user."""

    def __init__(self):
        self.api = get_tyk_users_admin_api()
        self.user: TykUserModel | None = None

    async def __aenter__(self) -> TykUserModel:
        temp_email = f"temp_admin_{random.randint(10000, 99999)}@example.com"
        temp_user = TykUserGenerator.generate_super_admin_user(email_address=temp_email)
        self.user = await self.api.create_user(temp_user)
        return self.user

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not (self.user and self.user.id):
            return

        try:
            await get_tyk_users_api(self.user.access_key or "").delete_user(self.user)
        except Exception as e:
            logger.warning(f"Failed to delete temporary super admin user {self.user.email_address}: {e}")
        finally:
            self.user = None


class TykMasterUsersRepository:
    """Handles super admin and org admin user management."""

    def __init__(self):
        self.api = get_tyk_users_admin_api()
        self.super_admin_access_key: str | None = None

    # ---------------------------
    # Super Admin Handling
    # ---------------------------

    async def get_access_key(self) -> str | None:
        await self.ensure_access_key()
        return self.super_admin_access_key

    def set_access_key(self, access_key: str | None) -> None:
        self.super_admin_access_key = access_key

    async def bootstrap_super_admin(self) -> None:
        """Create a super admin user if none exists."""
        user = TykUserGenerator.generate_super_admin_user(
            email_address=settings.SUPER_ADMIN_EMAIL,
            password=settings.SUPER_ADMIN_PASSWORD,
        )
        created_user = await self.api.create_user(user)
        self.set_access_key(created_user.access_key)

    async def _fetch_super_admin_access_key_if_exists(self) -> str | None:
        """Try to find the super admin access key via a temporary admin context."""
        for _ in range(5):
            try:
                async with TempSuperAdminCTX() as temp_admin:
                    user_api = get_tyk_users_api(temp_admin.access_key or "")
                    all_users = await user_api.search_users(settings.SUPER_ADMIN_EMAIL)

                    for user in all_users or []:
                        if not user.org_id:  # indicates system-level super admin
                            return user.access_key

            except Exception as e:
                logger.error(f"Error fetching super admin access key: {e}")

        return None

    async def ensure_access_key(self) -> None:
        """Ensure that a valid super admin API key exists or create one if needed."""
        if self.super_admin_access_key:
            return

        access_key = await self._fetch_super_admin_access_key_if_exists()
        if access_key:
            self.set_access_key(access_key)
            return

        await self.bootstrap_super_admin()

    # ---------------------------
    # Org Admin Handling
    # ---------------------------

    async def bootstrap_org_admin(self, org_id: str) -> TykUserModel:
        """Create an org admin user for a given organization."""
        users_api = get_tyk_users_api(self.super_admin_access_key or "")
        users_repo = TykUsersRepository(users_api, self.api)

        org_admin_user = TykUserGenerator.generate_org_admin_user(
            password=settings.ORG_ADMIN_PASSWORD,
            org_id=org_id,
            email_address=settings.ORG_ADMIN_EMAIL,
        )

        return await users_repo.create_user(org_admin_user)

    async def get_org_admin_api_key(self, org_id: str) -> str | None:
        """Return the org admin API key for an org, creating it if needed."""
        users_api = get_tyk_users_api(self.super_admin_access_key or "")
        users_repo = TykUsersRepository(users_api, self.api)

        org_users = await users_repo.get_users_by_organization(org_id)

        for user in org_users:
            if user.email_address == settings.ORG_ADMIN_EMAIL:
                return user.access_key

        user = await self.bootstrap_org_admin(org_id)
        return user.access_key if user else None
