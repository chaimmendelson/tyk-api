from .base import TykDashboardRepository
from ..api import TykUserGroupsAPI
from .usergroups import TykUserGroupsRepository
from ..generators import TykUserGroupGenerator
from ..errors import TykAPIWrapperError, TykNotFoundError
from ..settings import settings

OBJ_NAME = "application"
PREFIX = settings.syntax.APPLICATION_USERGROUP_PREFIX

class TykApplicationsRepository(TykDashboardRepository[TykUserGroupsAPI]):
    
    api_cls = TykUserGroupsAPI

    def __init__(self, api: TykUserGroupsAPI, org_id: str):
        super().__init__(api, org_id)
        self.usergroup_repo = TykUserGroupsRepository(api, org_id)

    async def get_applications(self) -> list[str]:
        usergroups = await self.usergroup_repo.get_usergroups()
        
        app_usergroups = [
            ug.name for ug in usergroups if ug.name and ug.name.startswith(PREFIX)
        ]
        
        return [ug_name.removeprefix(PREFIX) for ug_name in app_usergroups]
    
    async def create_application_usergroup(self, app_name: str) -> str:
        
        usergroup_model = await self.usergroup_repo.create_usergroup(
            usergroup=TykUserGroupGenerator.generate_application_usergroup(app_name)
        )
        
        if not usergroup_model.name:
            raise TykAPIWrapperError(f"Failed to create user group for application '{app_name}'")
        
        return usergroup_model.name
    
    async def delete_application_usergroup(self, app_name: str) -> None:
        
        usergroup_name = f"{PREFIX}{app_name}"
        
        usergroup = await self.usergroup_repo.get_usergroup_by_name(usergroup_name)
        
        await self.usergroup_repo.delete_usergroup(usergroup)
    
    async def application_usergroup_exists(self, app_name: str) -> bool:
        
        usergroup_name = f"{PREFIX}{app_name}"
        
        try:
            await self.usergroup_repo.get_usergroup_by_name(usergroup_name)
            return True
        except TykNotFoundError:
            return False

    async def ensure_application_usergroup(self, app_name: str) -> None:
        if await self.application_usergroup_exists(app_name):
            await self.usergroup_repo.get_usergroup_by_name(f"{PREFIX}{app_name}")
        await self.create_application_usergroup(app_name)
