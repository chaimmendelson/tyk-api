import random
from typing import Self
from loguru import logger

from ..api import TykUsersApi, TykUsersAdminApi
from ..settings import settings
from ..models import TykUserModel
from ..generators import TykUserGenerator
from ..errors import TykAPIError


class TempSuperAdminCTX:
    """Async context manager for creating and cleaning up a temporary super admin user."""

    def __init__(self):
        self.api: TykUsersAdminApi = TykUsersAdminApi.instance()
        self.user: TykUserModel | None = None

    def get_users_api(self) -> TykUsersApi:
        if not self.user or not self.user.access_key:
            raise ValueError("Temporary user or access key is not set.")
        logger.debug(f"Creating TykUsersApi with temporary admin key for user {self.user.email_address}")
        return TykUsersApi.instance(key=self.user.access_key)

    async def __aenter__(self) -> Self:
        temp_username = f"temp_admin_{random.randint(10000, 99999)}"
        logger.debug(f"Creating temporary super admin user: {temp_username}")
        temp_user = TykUserGenerator.generate_super_admin_user(username=temp_username)
        self.user = await self.api.create_user(temp_user)
        logger.debug(f"Temporary super admin {self.user.email_address} created successfully.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self.user:
            logger.debug("No temporary user found to delete on context exit.")
            return

        logger.debug(f"Deleting temporary super admin user: {self.user.email_address}")
        try:
            await TykUsersApi.instance(key=self.user.access_key or "").delete_user(self.user)
            logger.debug(f"Temporary super admin user {self.user.email_address} deleted successfully.")
        except Exception as e:
            logger.warning(f"Failed to delete temporary super admin user {self.user.email_address}: {e}")
        finally:
            self.user = None
            logger.debug("Temporary super admin context cleaned up.")


class TykMasterUsersRepository:
    """Handles super admin and org admin user management."""

    def __init__(self, api: TykUsersAdminApi):
        self.api = api
        self.super_admin: TykUserModel | None = None

    @classmethod
    def instance(cls) -> "TykMasterUsersRepository":
        logger.debug("Initializing TykMasterUsersRepository instance.")
        api = TykUsersAdminApi.instance()
        return cls(api=api)

    # ---------------------------
    # Super Admin Handling
    # ---------------------------

    async def get_super_admin_key(self) -> str:
        """Return the super admin API key, ensuring the user exists."""
        logger.debug("Retrieving super admin API key.")
        user = await self.ensure_user()
        key = user.get_access_key
        logger.debug(f"Super admin API key retrieved for {user.email_address[:3]}***")
        return key

    async def get_super_admin_api(self) -> TykUsersApi:
        logger.debug("Initializing TykUsersApi for super admin.")
        api_key = await self.get_super_admin_key()
        api = TykUsersApi.instance(
            key=api_key,
            override_base_url=self.api.api.base_url,
        )
        logger.debug("Super admin TykUsersApi instance created.")
        return api

    async def bootstrap_super_admin(self) -> TykUserModel:
        """Create a super admin user if none exists."""
        logger.debug("Bootstrapping super admin user...")
        user = TykUserGenerator.generate_super_admin_user(
            username=settings.SUPER_ADMIN_USERNAME,
            password=settings.SUPER_ADMIN_PASSWORD,
        )

        created_user = await self.api.create_user(user)
        self.super_admin = created_user

        logger.debug(f"Super admin user '{created_user.email_address}' created successfully.")
        return created_user

    async def find_super_admin(self) -> TykUserModel:
        """Try to find the super admin user via a temporary admin context."""
        logger.debug("Searching for existing super admin user.")
        for attempt in range(1, 6):
            try:
                logger.debug(f"Attempt {attempt}/5 to find super admin user.")
                async with TempSuperAdminCTX() as temp_admin:
                    users_api = temp_admin.get_users_api()
                    users = await users_api.search_users(settings.SUPER_ADMIN_USERNAME)
                    if not users:
                        logger.debug("No users found matching super admin username.")
                        continue
                    for user in users:
                        if not user.org_id:
                            logger.debug(f"Super admin user found: {user.email_address}")
                            return user
            except Exception as e:
                logger.warning(f"Error fetching super admin access key (attempt {attempt}): {e}")

        logger.error("Failed to fetch super admin access key after multiple attempts.")
        raise TykAPIError("Failed to fetch super admin access key after multiple attempts.")

    async def ensure_user(self) -> TykUserModel:
        """Ensure that a valid super admin exists or create one if needed."""
        if self.super_admin:
            logger.debug(f"Using cached super admin: {self.super_admin.email_address}")
            return self.super_admin

        try:
            logger.debug("Attempting to find existing super admin...")
            self.super_admin = await self.find_super_admin()
        except Exception as e:
            logger.warning(f"Super admin not found, bootstrapping a new one: {e}")
            self.super_admin = await self.bootstrap_super_admin()

        if not self.super_admin:
            logger.error("Failed to ensure super admin user exists.")
            raise TykAPIError("Failed to ensure super admin user exists.")

        logger.debug(f"Super admin user ensured: {self.super_admin.email_address}")
        return self.super_admin

    # ---------------------------
    # Org Admin Handling
    # ---------------------------

    async def bootstrap_org_admin(self, org_id: str) -> TykUserModel:
        """Create an org admin user for a given organization."""
        logger.debug(f"Bootstrapping org admin for organization {org_id}...")
        org_admin_user = TykUserGenerator.generate_org_admin_user(
            username=settings.ORG_ADMIN_USERNAME,
            password=settings.ORG_ADMIN_PASSWORD,
            org_id=org_id,
        )
        created_user = await self.api.create_user(org_admin_user)
        logger.debug(f"Org admin user created for organization {org_id}.")
        return created_user

    async def get_org_admin(self, org_id: str) -> TykUserModel:
        """Return the org admin API key for an org, creating it if needed."""
        logger.debug(f"Fetching org admin user for org {org_id}.")
        users_api = await self.get_super_admin_api()
        all_users = await users_api.search_users(settings.ORG_ADMIN_USERNAME)

        for user in all_users or []:
            if user.org_id == org_id:
                logger.debug(f"Existing org admin found for org {org_id}: {user.email_address}")
                return user

        logger.warning(f"No org admin found for org {org_id}, creating a new one.")
        user = await self.bootstrap_org_admin(org_id)
        return user

    async def get_org_admin_key(self, org_id: str) -> str:
        """Return the org admin API key for an org, creating it if needed."""
        logger.debug(f"Retrieving org admin API key for org {org_id}.")
        user = await self.get_org_admin(org_id)
        key = user.get_access_key
        logger.debug(f"Org admin API key retrieved for org {org_id}.")
        return key
