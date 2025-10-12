import random
from horizon_fastapi_template.utils import BaseAPI
from loguru import logger
from src.api.dashboard.users import TykUsersApi
from src.settings import settings
from src.api import TykUsersAdminApi
from src.models import TykUserModel
from .users import TykUsersRepository
from .base import TykRepository
from src.generators import TykUserGenerator

def get_tyk_api(api_key: str) -> BaseAPI:
    return BaseAPI(
        base_url=settings.DASHBOARD_URL,
        headers={
            "Authorization": api_key,
        },
    )

class TempSuperAdminCTX:
    def __init__(self, api: TykUsersAdminApi):
        self.api = api
        self.user: TykUserModel | None = None
        
    async def __aenter__(self) -> TykUserModel:
        temp_email = f"temp_admin_{random.randint(10000, 99999)}@example.com"
        
        temp_user = TykUserGenerator.generate_super_admin_user(
            email_address=temp_email,
        )
        
        self.user = await self.api.create_user(temp_user)
        return self.user
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.user and self.user.id:
            
            api = TykUsersApi(get_tyk_api(self.user.access_key or ""))
            
            await api.delete_user(self.user)
            
        self.user = None
        
class TykMasterUsersRepository(TykRepository):
    
    def __init__(self, api: TykUsersAdminApi):
        super().__init__(api)
        self.api = api
        self.super_admin_access_key: str | None = None

    async def get_access_key(self) -> str | None:
        await self.ensure_access_key()
        return self.super_admin_access_key

    def set_access_key(self, access_key: str | None) -> None:
        self.super_admin_access_key = access_key
    
    async def bootstrap_super_admin(self) -> None:
        user = TykUserGenerator.generate_super_admin_user(
            email_address=settings.SUPER_ADMIN_EMAIL,
            password=settings.SUPER_ADMIN_PASSWORD,
        )
        
        user = await self.api.create_user(user)

        self.set_access_key(user.access_key)

    async def _fetch_super_admin_access_key_if_exists(self) -> str | None:
        
        for _ in range(5):
            try:
                async with TempSuperAdminCTX(self.api) as temp_admin:

                    user_api = TykUsersApi(get_tyk_api(temp_admin.access_key or ""))

                    all_users = await user_api.search_users(settings.SUPER_ADMIN_EMAIL)
                        
                    for user in all_users or []:
                        if not user.org_id:
                            return user.access_key
                  
                return None

            except Exception as e:
                logger.error(f"Error fetching super admin access key: {e}")
                continue
            
    async def ensure_access_key(self) -> None:
        
        if self.super_admin_access_key is not None:
            return
        
        access_key = await self._fetch_super_admin_access_key_if_exists()
        
        if access_key:
            self.set_access_key(access_key)
            return
        
        await self.bootstrap_super_admin()

    async def bootstrap_org_admin(self, org_id: str) -> TykUserModel:
        users_api = TykUsersApi(get_tyk_api(self.super_admin_access_key or ""))
        users_repo = TykUsersRepository(users_api, self.api)
        
        org_admin_user = TykUserGenerator.generate_org_admin_user(
            password=settings.ORG_ADMIN_PASSWORD,
            org_id=org_id,
            email_address=settings.ORG_ADMIN_EMAIL,
        )
        
        created_user = await users_repo.create_user(org_admin_user)

        return created_user

    async def get_org_admin_api_key(self, org_id: str) -> str | None:
        users_api = TykUsersApi(get_tyk_api(self.super_admin_access_key or ""))
        users_repo = TykUsersRepository(users_api, self.api)
        
        org_users = await users_repo.get_users_by_organization(org_id)
        
        for user in org_users:
            if user.email_address == settings.ORG_ADMIN_EMAIL:
                return user.access_key
            
        user = await self.bootstrap_org_admin(org_id)

        if user is not None:
            return user.access_key or None

        return None