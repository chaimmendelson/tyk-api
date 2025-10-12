from tyk_api.src.api import TykUsersAdminApi, TykUsersApi
from tyk_api.src.models import TykUserModel
from .base import TykHybridRepository

class TykUsersRepository(TykHybridRepository[TykUsersApi, TykUsersAdminApi]):

    admin_api_cls = TykUsersAdminApi
    dashboard_api_cls = TykUsersApi
    
    def __init__(self, dashboard_api: TykUsersApi, admin_api: TykUsersAdminApi):
        super().__init__(
            dashboard_api=dashboard_api,
            admin_api=admin_api,
        )
        
    async def create_user(self, user: TykUserModel) -> TykUserModel:
        return await self.admin_api.create_user(user)

    async def get_users(self) -> list[TykUserModel]:
        return await self.dashboard_api.get_users()
    
    async def get_user_by_id(self, user_id: str) -> TykUserModel | None:
        return await self.dashboard_api.get_user(user_id)

    async def get_users_by_email(self, email: str) -> list[TykUserModel]:
        
        users = await self.get_users()
        
        return [user for user in users if user.email_address == email]
    
    async def get_users_by_organization(self, org_id: str) -> list[TykUserModel]:
        
        users = await self.get_users()
        
        return [user for user in users if user.org_id == org_id]
    
    async def get_user_by_email_and_organization(self, email: str, org_id: str) -> TykUserModel | None:
        
        users = await self.get_users_by_email(email)
        
        for user in users:
            if user.org_id == org_id:
                return user
        
        return None
    
    async def update_user(self, user: TykUserModel) -> TykUserModel:
        return await self.admin_api.update_user(user)

    async def delete_user(self, user: TykUserModel) -> None:
        await self.dashboard_api.delete_user(user)
    
    async def reset_user_api_key(self, user: TykUserModel) -> None:
        await self.dashboard_api.reset_user_api_key(user)
        
    async def revoke_user(self, user: TykUserModel) -> None:
        await self.dashboard_api.revoke_user(user)
        
    async def get_self(self) -> TykUserModel:
        return await self.dashboard_api.get_self()