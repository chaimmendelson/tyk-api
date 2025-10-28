from tyk_api.src.api import TykUserGroupsAPI
from tyk_api.src.generators import TykUserGroupGenerator
from tyk_api.src.models import TykUserGroupModel, MainUserGroups, TykUserGroupCreateModel, TykUserGroupUpdateModel
from .base import TykDashboardRepository
from tyk_api.src.errors import TykNameConflictError, TykNotFoundError, TykBadRequestError
from httpx import HTTPStatusError

OBJ_NAME = "User group"

class TykUserGroupsRepository(TykDashboardRepository[TykUserGroupsAPI]):

    api_cls = TykUserGroupsAPI

    def __init__(self, api: TykUserGroupsAPI, org_id: str):
        super().__init__(api, org_id)

    async def get_usergroups(self) -> list[TykUserGroupModel]:
        usergroups = await self.api.get_usergroups()
        
        return [usergroup for usergroup in usergroups if usergroup.org_id == self.org_id]

    async def get_usergroup_by_id(self, usergroup_id: str) -> TykUserGroupModel:
        
        try:

            usergroup = await self.api.get_usergroup(usergroup_id)

            if usergroup.org_id != self.org_id:
                raise TykNotFoundError(OBJ_NAME, f"id='{usergroup_id}'")

            return usergroup

        except HTTPStatusError as e:
            
            if e.response.status_code == 404:
                raise TykNotFoundError(OBJ_NAME, f"id='{usergroup_id}'")
            raise
    
    async def get_usergroup_by_name(self, name: str) -> TykUserGroupModel:
        usergroups = await self.get_usergroups()

        for usergroup in usergroups:
            if usergroup.name == name:
                return usergroup

        raise TykNotFoundError(OBJ_NAME, f"name='{name}'")

    async def create_usergroup(self, usergroup: TykUserGroupCreateModel) -> TykUserGroupModel:

        if not usergroup.name or not usergroup.name.strip():
            raise TykBadRequestError(f"{OBJ_NAME} name cannot be empty.")

        try:
            
            existing_ug = await self.get_usergroup_by_name(usergroup.name)
            
            if existing_ug:
                raise TykNameConflictError("user group", usergroup.name)
            
        except TykNotFoundError:
            pass  # User group does not exist, which is expected
        
        return await self.api.create_usergroup(usergroup)

    async def update_usergroup(self, usergroup: TykUserGroupUpdateModel) -> None:

        if not usergroup.name or not usergroup.name.strip():
            raise TykBadRequestError(f"{OBJ_NAME} name cannot be empty.")
        
        await self.api.update_usergroup(usergroup)

    async def delete_usergroup(self, usergroup: TykUserGroupModel) -> None:
        await self.api.delete_usergroup(usergroup)

    async def get_main_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        
        return await self.get_usergroup_by_name(usergroup.value)

    async def create_main_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        usergroup_model = TykUserGroupGenerator.generate_main_usergroups(usergroup)
        return await self.create_usergroup(usergroup_model)

    async def update_main_usergroup(self, usergroup: MainUserGroups) -> None:
        existing_usergroup = await self.get_main_usergroup(usergroup)

        usergroup_model = TykUserGroupGenerator.generate_main_usergroup_update(usergroup, existing_usergroup.id)

        await self.update_usergroup(usergroup_model)

    async def delete_main_usergroup(self, usergroup: MainUserGroups) -> None:
        existing_usergroup = await self.get_main_usergroup(usergroup)
        await self.delete_usergroup(existing_usergroup)

    async def ensure_main_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        try:
            return await self.get_main_usergroup(usergroup)
        except TykNotFoundError:
            return await self.create_main_usergroup(usergroup)
    
    async def ensure_main_usergroup_and_update(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        try:
            existing_ug = await self.get_main_usergroup(usergroup)
            await self.update_main_usergroup(usergroup)
            return existing_ug
        except TykNotFoundError:
            return await self.create_main_usergroup(usergroup)
    
    
    