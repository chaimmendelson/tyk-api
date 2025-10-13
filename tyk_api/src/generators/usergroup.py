from tyk_api.src.models import (
    TykUserGroupModel,
    TykUserGroupPermissions,
    MainUserGroups
)



class TykUserGroupGenerator:

    @staticmethod
    def generate_from_main_usergroups(main_group: MainUserGroups):
        return TykUserGroupGenerator.generate_usergroup(main_group.permissions, main_group.value)

    @staticmethod
    def generate_usergroup(permissions: TykUserGroupPermissions, name: str):
        return TykUserGroupModel(
            name=name,
            user_permissions=permissions
        )