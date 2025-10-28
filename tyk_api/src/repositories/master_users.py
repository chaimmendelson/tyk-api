import random
from typing import Self
from loguru import logger

from tyk_api.src.api import TykUsersApi, TykUsersAdminApi
from tyk_api.src.settings import settings
from tyk_api.src.models import TykUserModel
from tyk_api.src.generators import TykUserGenerator


class TempSuperAdminCTX:
    """Async context manager for creating and cleaning up a temporary super admin user."""

    def __init__(self):
        self.api: TykUsersAdminApi = TykUsersAdminApi.instance()
        self.user: TykUserModel | None = None

    def get_users_api(self) -> TykUsersApi:
        if not self.user or not self.user.access_key:
            raise ValueError("Temporary user or access key is not set.")
        return TykUsersApi.instance(key=self.user.access_key)

    async def __aenter__(self) -> Self:
        temp_username = f"temp_admin_{random.randint(10000, 99999)}"
        temp_user = TykUserGenerator.generate_super_admin_user(username=temp_username)
        self.user = await self.api.create_user(temp_user)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.user:
            return
        try:
            await TykUsersApi.instance(key=self.user.access_key or "").delete_user(self.user)
        except Exception as e:
            logger.warning(f"Failed to delete temporary super admin user {self.user.email_address}: {e}")
        finally:
            self.user = None


class TykMasterUsersRepository():
    """Handles super admin and org admin user management."""
    
    def __init__(self, api: TykUsersAdminApi):
        self.api = api
        self.super_admin: TykUserModel | None = None
    
    @classmethod
    async def instance(cls) -> "TykMasterUsersRepository":
        api = TykUsersAdminApi.instance()
        return cls(api=api)
    
    # ---------------------------
    # Super Admin Handling
    # ---------------------------

    async def get_super_admin_key(self) -> str:
        """Return the super admin API key, ensuring the user exists."""
        await self.ensure_user()
        if not self.super_admin:
            raise ValueError("Super admin user is not set.")
        return self.super_admin.get_access_key

    async def get_super_admin_api(self) -> TykUsersApi:
        return TykUsersApi.instance(
            key=await self.get_super_admin_key(),
            override_base_url=self.api.api.base_url
        )

    async def bootstrap_super_admin(self) -> None:
        """Create a super admin user if none exists."""
        user = TykUserGenerator.generate_super_admin_user(
            username=settings.SUPER_ADMIN_USERNAME,
            password=settings.SUPER_ADMIN_PASSWORD,
        )
        self.super_admin = await self.api.create_user(user)

    async def find_super_admin(self) -> TykUserModel:
        """Try to find the super admin user via a temporary admin context."""
        for _ in range(5):
            try:
                async with TempSuperAdminCTX() as temp_admin:
                    users_api = temp_admin.get_users_api()
                    users = await users_api.search_users(settings.SUPER_ADMIN_USERNAME)
                    for user in users or []:
                        if not user.org_id:
                            return user
            except Exception as e:
                logger.warning(f"Error fetching super admin access key: {e}")
        raise ValueError("Failed to fetch super admin access key after multiple attempts.")

    async def ensure_user(self) -> None:
        """Ensure that a valid super admin exists or create one if needed."""
        if self.super_admin:
            return
        try:
            self.super_admin = await self.find_super_admin()
            
        except Exception:
            await self.bootstrap_super_admin()

    # ---------------------------
    # Org Admin Handling
    # ---------------------------

    async def bootstrap_org_admin(self, org_id: str) -> TykUserModel:
        """Create an org admin user for a given organization."""
        org_admin_user = TykUserGenerator.generate_org_admin_user(
            username=settings.ORG_ADMIN_USERNAME,
            password=settings.ORG_ADMIN_PASSWORD,
            org_id=org_id,
        )
        return await self.api.create_user(org_admin_user)

    async def get_org_admin(self, org_id: str) -> TykUserModel:
        """Return the org admin API key for an org, creating it if needed."""
        users_api = await self.get_super_admin_api()
        all_users = await users_api.search_users(settings.ORG_ADMIN_USERNAME)

        for user in all_users or []:
            if user.org_id == org_id:
                return user

        user = await self.bootstrap_org_admin(org_id)
        return user
    
    async def get_org_admin_key(self, org_id: str) -> str:
        """Return the org admin API key for an org, creating it if needed."""
        user = await self.get_org_admin(org_id)
        
        return user.get_access_key
