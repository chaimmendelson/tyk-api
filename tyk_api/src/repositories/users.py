from ..api import TykUsersAdminApi, TykUsersApi
from ..models import (
    TykUserModel,
    TykUserCreateModel,
    TykUserUpdateModel,
)

from .base import TykHybridRepository


class TykUsersRepository(TykHybridRepository[TykUsersApi, TykUsersAdminApi]):
    """Repository for managing Tyk users through both Admin and Dashboard APIs."""

    admin_api_cls = TykUsersAdminApi
    dashboard_api_cls = TykUsersApi

    def __init__(self, dashboard_api: TykUsersApi, admin_api: TykUsersAdminApi, org_id: str):
        super().__init__(dashboard_api=dashboard_api, admin_api=admin_api, org_id=org_id)

    # ──────────────────────────────── CRUD METHODS ────────────────────────────────

    async def create_user(self, user: TykUserCreateModel) -> TykUserModel:
        return await self.admin_api.create_user(user)

    async def get_users(self) -> list[TykUserModel]:
        return await self.dashboard_api.get_users()

    async def get_user_by_id(self, user_id: str) -> TykUserModel:
        return await self.dashboard_api.get_user(user_id)

    async def update_user(self, user: TykUserUpdateModel) -> TykUserModel:
        return await self.admin_api.update_user(user)

    async def delete_user(self, user: TykUserModel) -> None:
        await self.dashboard_api.delete_user(user)

    # ──────────────────────────────── SEARCH HELPERS ────────────────────────────────

    async def get_users_by_email(self, email: str) -> list[TykUserModel]:
        users = await self.get_users()
        return [user for user in users if user.email_address == email]

    async def get_users_by_organization(self, org_id: str) -> list[TykUserModel]:
        users = await self.get_users()
        return [user for user in users if user.org_id == org_id]

    async def get_user_by_email_and_organization(self, email: str, org_id: str) -> TykUserModel | None:
        users = await self.get_users_by_email(email)
        return next((user for user in users if user.org_id == org_id), None)

    # ──────────────────────────────── USER ACTIONS ────────────────────────────────

    async def reset_user_api_key(self, user: TykUserModel) -> None:
        await self.dashboard_api.reset_user_api_key(user)

    async def revoke_user(self, user: TykUserModel) -> None:
        await self.dashboard_api.revoke_user(user)

    async def get_self(self) -> TykUserModel:
        return await self.dashboard_api.get_self()
