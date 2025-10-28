from httpx import HTTPStatusError
from ..base import BaseAPI, TykDashboardApi
from tyk_api.src.models import TykUserGroupModel, TykUserGroupCreateModel, TykUserGroupUpdateModel

USER_GROUPS_KEY = "groups"

class TykUserGroupsAPI(TykDashboardApi):
    
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/usergroups",
    ):
        super().__init__(api, base_uri)
        
    async def get_usergroups(self) -> list[TykUserGroupModel]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()

        user_groups_data = response.json().get(USER_GROUPS_KEY, []) or []

        return [TykUserGroupModel.model_validate(group) for group in user_groups_data]

    async def get_usergroup(self, group_id: str) -> TykUserGroupModel:
        response = await self.api.client.get(f"{self.base_uri}/{group_id}")
        response.raise_for_status()
        
        return TykUserGroupModel.model_validate(response.json())

    async def create_usergroup(self, group: TykUserGroupCreateModel) -> TykUserGroupModel:
        
        body = group.model_dump(exclude_none=True)

        response = await self.api.client.post(self.base_uri, json=body)
        response.raise_for_status()
        
        group_id = response.json().get("Meta")

        return await self.get_usergroup(group_id)

    async def update_usergroup(self, group: TykUserGroupUpdateModel):
        
        body = group.model_dump(exclude_none=True)
        
        response = await self.api.client.put(f"{self.base_uri}/{group.id}", json=body)
        response.raise_for_status()

    async def delete_usergroup(self, group: TykUserGroupModel):
        response = await self.api.client.delete(f"{self.base_uri}/{group.id}")
        response.raise_for_status()