from tyk_api.src.models import (
    TykUserGroupCreateModel,
    TykUserGroupPermissions,
    MainUserGroups,
    TykUserGroupUpdateModel,
)
from ..models import TykPermissionLevel
from ..settings import settings

class TykUserGroupGenerator:

    @staticmethod
    def generate_main_usergroups(main_group: MainUserGroups) -> TykUserGroupCreateModel:
        return TykUserGroupGenerator.generate_usergroup(main_group.permissions, main_group.value)

    @staticmethod
    def generate_usergroup(permissions: TykUserGroupPermissions, name: str) -> TykUserGroupCreateModel:
        return TykUserGroupCreateModel(
            name=name,
            user_permissions=permissions
        )
    
    @staticmethod
    def generate_application_usergroup(app_name: str) -> TykUserGroupCreateModel:
        prefix = settings.syntax.APPLICATION_USERGROUP_PREFIX
        usergroup_name = f"{prefix}{app_name}"
        permissions = TykUserGroupPermissions(system=TykPermissionLevel.DENY)
        return TykUserGroupGenerator.generate_usergroup(permissions, usergroup_name)

    @staticmethod
    def generate_usergroup_update(permissions: TykUserGroupPermissions, name: str, usergroup_id: str) -> TykUserGroupUpdateModel:
        return TykUserGroupUpdateModel(
            id=usergroup_id,
            name=name,
            user_permissions=permissions
        )
    
    @staticmethod
    def generate_main_usergroup_update(main_group: MainUserGroups, usergroup_id: str) -> TykUserGroupUpdateModel:
        return TykUserGroupGenerator.generate_usergroup_update(main_group.permissions, main_group.value, usergroup_id)
    