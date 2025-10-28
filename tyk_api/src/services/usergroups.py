from ..repositories import TykUserGroupsRepository
from ..models import TykUserGroupModel, MainUserGroups
from ..errors import TykNotFoundError, TykMultiOperationError
from loguru import logger


class UserGroupService:

    @staticmethod
    async def get_main_usergroup(main_group: MainUserGroups) -> TykUserGroupModel:
        logger.debug(f"Fetching main user group: {main_group.value}")
        repo = await TykUserGroupsRepository.instance(admin=True)
        
        group = await repo.ensure_main_usergroup(main_group)
        logger.info(f"Fetched main user group '{main_group.value}' successfully.")
        return group
    
    @staticmethod
    async def get_and_update_main_usergroup(main_group: MainUserGroups) -> TykUserGroupModel:
        logger.debug(f"Fetching and updating main user group: {main_group.value}")
        repo = await TykUserGroupsRepository.instance(admin=True)
        
        group = await repo.ensure_main_usergroup_and_update(main_group)
        logger.info(f"Fetched and updated main user group '{main_group.value}' successfully.")
        return group
    
    @staticmethod
    async def ensure_all_main_usergroups() -> None:
        logger.info("Ensuring all main user groups exist...")
        repo = await TykUserGroupsRepository.instance(admin=True)
        
        for group in MainUserGroups:
            try:
                await repo.ensure_main_usergroup(group)
                logger.debug(f"Ensured main user group '{group.value}' exists.")
            except Exception as e:
                logger.error(f"Failed to ensure main user group '{group.value}': {e}")
                raise
        logger.info("All main user groups ensured successfully.")
    
    @staticmethod
    async def delete_main_usergroup(main_group: MainUserGroups) -> None:
        logger.info(f"Deleting main user group: {main_group.value}")
        repo = await TykUserGroupsRepository.instance(admin=True)
        
        try:
            await repo.delete_main_usergroup(main_group)
            logger.info(f"Deleted main user group '{main_group.value}' successfully.")
        except TykNotFoundError:
            logger.warning(f"Main user group '{main_group.value}' not found for deletion.")
            raise
        except Exception as e:
            logger.error(f"Error deleting main user group '{main_group.value}': {e}")
            raise
    
    @staticmethod
    async def delete_all_main_usergroups() -> bool:
        logger.info("Deleting all main user groups...")
        repo = await TykUserGroupsRepository.instance(admin=True)
        
        success = True

        for group in MainUserGroups:
            try:
                await repo.delete_main_usergroup(group)
                logger.debug(f"Deleted main user group '{group.value}'.")
            except TykNotFoundError:
                logger.info(f"Main user group '{group.value}' not found for deletion.")
            except Exception as e:
                logger.error(f"Error deleting main user group '{group.value}': {e}")
                success = False
        
        if success:
            logger.info("All main user groups deleted successfully.")
        else:
            logger.warning("Some main user groups failed to delete. See logs for details.")
        return success
    
    @staticmethod
    async def get_repo(org_id: str | None = None) -> TykUserGroupsRepository:
        logger.debug(f"Getting user group repository (org_id={org_id or 'admin'})")
        if not org_id:
            return await TykUserGroupsRepository.instance(admin=True)
        else:
            return await TykUserGroupsRepository.instance(org_id=org_id)
        
    @staticmethod
    async def list_all_usergroups(org_id: str) -> list[TykUserGroupModel]:
        logger.info(f"Listing all user groups for org: {org_id}")
        repo = await UserGroupService.get_repo(org_id=org_id)

        groups = await repo.get_usergroups()
        logger.debug(f"Found {len(groups)} user groups for org '{org_id}'.")
        return groups
    
    @staticmethod
    async def delete_usergroup_by_id(org_id: str, usergroup_id: str) -> None:
        logger.info(f"Deleting user group '{usergroup_id}' from org '{org_id}'")
        repo = await UserGroupService.get_repo(org_id=org_id)
        
        try:
            usergroup = await repo.get_usergroup_by_id(usergroup_id)
            await repo.delete_usergroup(usergroup)
            logger.info(f"Deleted user group '{usergroup.name}' ({usergroup_id}) successfully.")
        except TykNotFoundError:
            logger.warning(f"User group '{usergroup_id}' not found in org '{org_id}'.")
            raise
        except Exception as e:
            logger.error(f"Error deleting user group '{usergroup_id}' from org '{org_id}': {e}")
            raise
        
    @staticmethod
    async def delete_all_usergroups(org_id: str) -> None:
        logger.info(f"Deleting all user groups for org '{org_id}'")
        repo = await UserGroupService.get_repo(org_id=org_id)
        
        usergroups = await repo.get_usergroups()
        logger.debug(f"Found {len(usergroups)} user groups to delete in org '{org_id}'.")

        errors: dict[str, str] = {}

        for ug in usergroups:
            try:
                await UserGroupService.delete_usergroup_by_id(org_id, ug.id)
            except Exception as e:
                logger.error(f"Error deleting user group '{ug.name}' ({ug.id}): {e}")
                errors[ug.id] = str(e)

        if errors:
            logger.error(f"Errors occurred while deleting user groups for org '{org_id}': {errors}")
            raise TykMultiOperationError("Errors occurred while deleting user groups", errors)
        
        logger.info(f"All user groups for org '{org_id}' deleted successfully.")
