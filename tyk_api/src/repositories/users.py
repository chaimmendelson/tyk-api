from ..api import TykUsersAdminApi, TykUsersApi
from ..models import (
    TykUserModel,
    TykUserCreateModel,
    TykUserUpdateModel,
)

from .base import TykHybridRepository
from ..errors import TykNotFoundError, TykFailedToCreateError
from httpx import HTTPStatusError


RESOURCE = "User"


class TykUsersRepository(TykHybridRepository[TykUsersApi, TykUsersAdminApi]):
    """Repository for managing Tyk users through both Admin and Dashboard APIs."""

    admin_api_cls = TykUsersAdminApi
    dashboard_api_cls = TykUsersApi

    def __init__(
        self, dashboard_api: TykUsersApi, admin_api: TykUsersAdminApi, org_id: str
    ):
        super().__init__(
            dashboard_api=dashboard_api, admin_api=admin_api, org_id=org_id
        )

    # ──────────────────────────────── CRUD METHODS ────────────────────────────────

    async def create_user(self, user: TykUserCreateModel) -> TykUserModel:

        try:

            return await self.admin_api.create_user(user)

        except Exception as e:
            raise TykFailedToCreateError(RESOURCE, str(e))

    async def get_users(self) -> list[TykUserModel]:
        return await self.dashboard_api.get_users()

    async def get_user_by_id(self, user_id: str) -> TykUserModel:

        user = await self.dashboard_api.get_user(user_id)

        if not user:
            raise TykNotFoundError(RESOURCE, user_id)

        return user

    async def update_user(self, user: TykUserUpdateModel) -> TykUserModel:
        
        try:
            return await self.admin_api.update_user(user)
        except HTTPStatusError as e:
            super().handle_response_error(e, RESOURCE, f"{user.id=}")
            raise e

    async def delete_user(self, user: TykUserModel) -> None:

        try:
            await self.dashboard_api.delete_user(user)
        except HTTPStatusError as e:
            super().handle_response_error(e, RESOURCE, f"{user.id=}")

    # ──────────────────────────────── SEARCH HELPERS ────────────────────────────────

    async def get_users_by_email(self, email: str) -> list[TykUserModel]:
        users = await self.get_users()
        return [user for user in users if user.email_address == email]

    async def get_users_by_organization(self, org_id: str) -> list[TykUserModel]:
        users = await self.get_users()
        return [user for user in users if user.org_id == org_id]

    async def get_user_by_email_and_organization(
        self, email: str, org_id: str
    ) -> TykUserModel:
        
        users = await self.get_users_by_email(email)
        user = next((user for user in users if user.org_id == org_id), None)

        if not user:
            raise TykNotFoundError(RESOURCE, f"email: {email}, org_id: {org_id}")

        return user

    # ──────────────────────────────── USER ACTIONS ────────────────────────────────

    async def reset_user_api_key(self, user: TykUserModel) -> None:
        try:
            await self.dashboard_api.reset_user_api_key(user)
        except HTTPStatusError as e:
            super().handle_response_error(e, RESOURCE, f"{user.id=}")

    async def revoke_user(self, user: TykUserModel) -> None:
        
        try:
            await self.dashboard_api.revoke_user(user)
        except HTTPStatusError as e:
            super().handle_response_error(e, RESOURCE, f"{user.id=}")

    async def get_self(self) -> TykUserModel:
        return await self.dashboard_api.get_self()

    async def delete_user_by_email(self, email: str, org_id: str) -> None:
        
        user = await self.get_user_by_email_and_organization(email, org_id)
        
        await self.delete_user(user)

    async def change_user_password(self, user: TykUserUpdateModel, new_password: str) -> None:
        try:
            user.password = new_password
            await self.update_user(user)
        except HTTPStatusError as e:
            super().handle_response_error(e, RESOURCE, f"{user.id=}")
