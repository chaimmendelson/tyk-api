from ..base import BaseAPI, TykDashboardAdminApi
from tyk_api.src.models import TykUserModel


class TykUsersAdminApi(TykDashboardAdminApi):

    def __init__(self, api: BaseAPI, base_uri: str = "/admin/users"):
        super().__init__(api, base_uri)

    async def create_user(self, user: TykUserModel) -> TykUserModel:
        body = user.model_dump(exclude_none=True, exclude={"password"}, mode="json")

        response = await self.api.client.post(self.base_uri, json=body)

        response.raise_for_status()

        created_user = TykUserModel.model_validate(response.json().get("Meta", {}) or {})

        if user.password is not None:
            created_user.password = user.password

            return await self.update_user(created_user)

        return created_user



    async def update_user(self, user: TykUserModel) -> TykUserModel:

        if user.id is None:
            raise ValueError("User ID is required for update")

        body = user.model_dump(exclude_none=True, mode="json")

        response = await self.api.client.put(f"{self.base_uri}/{user.id}", json=body)

        response.raise_for_status()

        return user
