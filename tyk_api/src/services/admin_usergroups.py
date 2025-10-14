import asyncio

from ..repositories import get_tyk_usergroups_repository, TykUserGroupsRepository
from ..settings import settings
from ..models import TykUserGroupModel, MainUserGroups
from ..generators import TykUserGroupGenerator
from ..errors import TykAPIError, TykNameConflictError
from loguru import logger


USERGROUPS_REPO_NOT_INITIALIZED_MSG = "User groups repository not initialized."

class AdminUserGroupService:

    def __init__(self):
        self.repo: TykUserGroupsRepository | None = None

    async def _initialize_repo(self) -> None:
        if not self.repo:
            self.repo = await get_tyk_usergroups_repository()

    async def get_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel | None:
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        usergroups = await self.repo.get_usergroups_by_name(usergroup.value)
        
        return usergroups[0] if usergroups else None
    
    async def _create_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        usergroup_model = TykUserGroupGenerator.generate_from_main_usergroups(usergroup)
        
        try:
            return await self.repo.create_usergroup(usergroup_model)
        except TykNameConflictError:
            raise TykAPIError(f"User group with name '{usergroup.value}' already exists.")

    async def _update_usergroup(self, usergroup: MainUserGroups) -> None:
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        existing_usergroup = await self.get_usergroup(usergroup)

        if not existing_usergroup or not existing_usergroup.id:
            raise TykAPIError(f"User group '{usergroup.value}' does not exist.")
        
        usergroup_model = TykUserGroupGenerator.generate_from_main_usergroups(usergroup)
        usergroup_model.id = existing_usergroup.id
        
        await self.repo.update_usergroup(usergroup_model)
        
    async def _delete_usergroup(self, usergroup: MainUserGroups) -> None:
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        existing_usergroup = await self.get_usergroup(usergroup)

        if not existing_usergroup:
            raise TykAPIError(f"User group '{usergroup.value}' does not exist.")
        
        await self.repo.delete_usergroup(existing_usergroup)
        
    async def _ensure_exists(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        existing_usergroup = await self.get_usergroup(usergroup)
        
        if existing_usergroup:
            return existing_usergroup
        
        return await self._create_usergroup(usergroup)

    async def update_admin_usergroups(self) -> None:
        await self._initialize_repo()
        
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        for usergroup in MainUserGroups:
            try:
                await self._ensure_exists(usergroup)
                await self._update_usergroup(usergroup)
            except TykAPIError as e:
                logger.error(f"Failed to update user group '{usergroup.value}': {e}")
    
    async def get_main_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel | None:
        await self._initialize_repo()
        
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        return await self.get_usergroup(usergroup)
    
    async def delete_main_usergroup(self, usergroup: MainUserGroups) -> None:
        await self._initialize_repo()
        
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        await self._delete_usergroup(usergroup)
        
    async def delete_all_main_usergroups(self) -> None:
        await self._initialize_repo()
        
        if not self.repo:
            raise TykAPIError(USERGROUPS_REPO_NOT_INITIALIZED_MSG)

        for usergroup in MainUserGroups:
            try:
                await self._delete_usergroup(usergroup)
            except TykAPIError as e:
                logger.error(f"Failed to delete user group '{usergroup.value}': {e}")
