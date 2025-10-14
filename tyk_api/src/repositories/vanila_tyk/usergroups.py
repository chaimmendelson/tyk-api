from tyk_api.src.api import TykUserGroupsAPI
from tyk_api.src.models import TykUserGroupModel
from .base import TykDashboardRepository
from tyk_api.src.errors import TykNameConflictError

class TykUserGroupsRepository(TykDashboardRepository[TykUserGroupsAPI]):

    api_cls = TykUserGroupsAPI
    
    def __init__(self, api: TykUserGroupsAPI):
        super().__init__(api)

    async def create_usergroup(self, usergroup: TykUserGroupModel) -> TykUserGroupModel:
        existing_usergroups = await self.get_usergroups_by_name(usergroup.name or "")
        
        if existing_usergroups:
            raise TykNameConflictError("usergroup", usergroup.name or "")
        
        return await self.api.create_usergroup(usergroup)
    
    async def get_usergroups(self) -> list[TykUserGroupModel]:
        return await self.api.get_usergroups()
    
    async def get_usergroups_by_name(self, name: str) -> list[TykUserGroupModel]:
        usergroups = await self.get_usergroups()
        
        return [ug for ug in usergroups if ug.name == name]
    
    async def get_usergroup_by_id(self, usergroup_id: str) -> TykUserGroupModel | None:
        return await self.api.get_usergroup(usergroup_id)

    async def update_usergroup(self, usergroup: TykUserGroupModel) -> None:
        await self.api.update_usergroup(usergroup)

    async def delete_usergroup(self, usergroup: TykUserGroupModel) -> None:
        await self.api.delete_usergroup(usergroup)