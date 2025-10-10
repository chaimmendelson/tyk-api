from horizon_fastapi_template.utils import BaseAPI
from src.models import TykUserGroupModel, TykUserGroupPermissions

USER_GROUPS_KEY = "groups"

class TykUserGroupsAPI:
    
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/usergroups",
    ):
        self.api = api
        self.base_uri = base_uri
        
    async def get_usergroups(self) -> list[TykUserGroupModel]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()

        user_groups_data = response.json().get(USER_GROUPS_KEY, [])

        return [TykUserGroupModel.model_validate(group) for group in user_groups_data]

    async def get_usergroup(self, group_id: str) -> TykUserGroupModel:
        response = await self.api.client.get(f"{self.base_uri}/{group_id}")
        response.raise_for_status()
        
        return TykUserGroupModel.model_validate(response.json())

    async def create_usergroup(self, group: TykUserGroupModel) -> TykUserGroupModel:
        
        body = group.model_dump(exclude_none=True)

        response = await self.api.client.post(self.base_uri, json=body)
        response.raise_for_status()
        
        group_id = response.json().get("Meta")
        
        if group_id is None:
            raise ValueError("Failed to create user group: Missing Meta field in response")
        
        group.id = group_id
        
        return group

    async def update_usergroup(self, group: TykUserGroupModel):
        
        body = group.model_dump(exclude_none=True)
        
        response = await self.api.client.put(f"{self.base_uri}/{group.id}", json=body)
        response.raise_for_status()

    async def delete_usergroup(self, group: TykUserGroupModel):
        response = await self.api.client.delete(f"{self.base_uri}/{group.id}")
        response.raise_for_status()