from ..base import BaseAPI, TykApi
from src.models import TykUserModel

USERS_KEY = "users"

class TykUsersApi(TykApi):
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/users",
    ):
        super().__init__(api, base_uri)

    async def get_users(self) -> list[TykUserModel]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()

        users_data = response.json().get(USERS_KEY, []) or []
        
        return [TykUserModel.model_validate(user) for user in users_data]

    async def get_user(self, user_id: str) -> TykUserModel:
        response = await self.api.client.get(f"{self.base_uri}/{user_id}")

        response.raise_for_status()

        return TykUserModel.model_validate(response.json())

    async def delete_user(self, user: TykUserModel):
        response = await self.api.client.delete(f"{self.base_uri}/{user.id}")

        response.raise_for_status()

    async def reset_user_api_key(self, user: TykUserModel):
        response = await self.api.client.put(f"{self.base_uri}/{user.id}/actions/key/reset")

        response.raise_for_status()

    async def revoke_user(self, user: TykUserModel):
        response = await self.api.client.put(f"{self.base_uri}/{user.id}/actions/revoke")

        response.raise_for_status()

    async def get_self(self) -> TykUserModel:
        response = await self.api.client.get(f"{self.base_uri}/me")

        response.raise_for_status()

        return TykUserModel.model_validate(response.json())
    
    async def search_users(self, query: str) -> list[TykUserModel]:

        body = {
            "filters": {
                "query": query
            }
        }

        response = await self.api.client.post(f"{self.base_uri}/search", json=body)

        response.raise_for_status()

        users_data = response.json().get(USERS_KEY, []) or []
        
        return [TykUserModel.model_validate(user) for user in users_data]
