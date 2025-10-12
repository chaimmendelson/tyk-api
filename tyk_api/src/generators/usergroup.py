from tyk_api.src.models import TykPermissionLevel, TykUserGroupModel, TykUserGroupPermissions

class TykUserGroupGenerator:

    @staticmethod
    def generate_basic_usergroup(name: str = "Basic User Group"):
        permissions = TykUserGroupPermissions(
            analytics=TykPermissionLevel.READ,
            api_assets=TykPermissionLevel.WRITE,
            apis=TykPermissionLevel.WRITE,
            audit_logs=TykPermissionLevel.READ,
            certs=TykPermissionLevel.DENY,
            hooks=TykPermissionLevel.WRITE,
            idm=TykPermissionLevel.DENY,
            keys=TykPermissionLevel.WRITE,
            log=TykPermissionLevel.READ,
            oauth=TykPermissionLevel.DENY,
            policies=TykPermissionLevel.WRITE,
            portal=TykPermissionLevel.DENY,
            system=TykPermissionLevel.DENY,
            user_groups=TykPermissionLevel.DENY,
            users=TykPermissionLevel.READ,
            websockets=TykPermissionLevel.WRITE
        )

        return TykUserGroupModel(
            name=name,
            user_permissions=permissions
        )

    @staticmethod
    def generate_read_only_usergroup(name: str = "Read-Only User Group"):
        permissions = TykUserGroupPermissions(
            analytics=TykPermissionLevel.READ,
            api_assets=TykPermissionLevel.READ,
            apis=TykPermissionLevel.READ,
            audit_logs=TykPermissionLevel.READ,
            certs=TykPermissionLevel.DENY,
            hooks=TykPermissionLevel.READ,
            idm=TykPermissionLevel.DENY,
            keys=TykPermissionLevel.READ,
            log=TykPermissionLevel.READ,
            oauth=TykPermissionLevel.DENY,
            policies=TykPermissionLevel.READ,
            portal=TykPermissionLevel.DENY,
            system=TykPermissionLevel.DENY,
            user_groups=TykPermissionLevel.DENY,
            users=TykPermissionLevel.READ,
            websockets=TykPermissionLevel.READ
        )

        return TykUserGroupModel(
            name=name,
            user_permissions=permissions
        )

    @staticmethod
    def generate_read_write_usergroup(name: str = "Read-Write User Group"):
        permmissions = TykUserGroupPermissions(
            analytics=TykPermissionLevel.READ,
            api_assets=TykPermissionLevel.WRITE,
            apis=TykPermissionLevel.WRITE,
            audit_logs=TykPermissionLevel.READ,
            certs=TykPermissionLevel.WRITE,
            hooks=TykPermissionLevel.WRITE,
            idm=TykPermissionLevel.WRITE,
            keys=TykPermissionLevel.WRITE,
            log=TykPermissionLevel.READ,
            oauth=TykPermissionLevel.WRITE,
            policies=TykPermissionLevel.WRITE,
            portal=TykPermissionLevel.WRITE,
            system=TykPermissionLevel.READ,
            user_groups=TykPermissionLevel.WRITE,
            users=TykPermissionLevel.WRITE,
            websockets=TykPermissionLevel.WRITE
        )

        return TykUserGroupModel(
            name=name,
            user_permissions=permmissions
        )

    @staticmethod
    def generate_no_access_usergroup(name: str = "No Access User Group"):
        permissions = TykUserGroupPermissions(
            analytics=TykPermissionLevel.DENY,
            api_assets=TykPermissionLevel.DENY,
            apis=TykPermissionLevel.DENY,
            audit_logs=TykPermissionLevel.DENY,
            certs=TykPermissionLevel.DENY,
            hooks=TykPermissionLevel.DENY,
            idm=TykPermissionLevel.DENY,
            keys=TykPermissionLevel.DENY,
            log=TykPermissionLevel.DENY,
            oauth=TykPermissionLevel.DENY,
            policies=TykPermissionLevel.DENY,
            portal=TykPermissionLevel.DENY,
            system=TykPermissionLevel.DENY,
            user_groups=TykPermissionLevel.DENY,
            users=TykPermissionLevel.DENY,
            websockets=TykPermissionLevel.DENY
        )

        return TykUserGroupModel(
            name=name,
            user_permissions=permissions
        )

    @staticmethod
    def generate_gateway_usergroup(name: str = "Gateway User Group"):
        permissions = TykUserGroupPermissions(
            analytics=TykPermissionLevel.DENY,
            api_assets=TykPermissionLevel.DENY,
            apis=TykPermissionLevel.READ,
            audit_logs=TykPermissionLevel.DENY,
            certs=TykPermissionLevel.DENY,
            hooks=TykPermissionLevel.READ,
            idm=TykPermissionLevel.DENY,
            keys=TykPermissionLevel.WRITE,
            log=TykPermissionLevel.DENY,
            oauth=TykPermissionLevel.WRITE,
            policies=TykPermissionLevel.READ,
            portal=TykPermissionLevel.DENY,
            system=TykPermissionLevel.DENY,
            user_groups=TykPermissionLevel.DENY,
            users=TykPermissionLevel.DENY,
            websockets=TykPermissionLevel.WRITE
        )

        return TykUserGroupModel(
            name=name,
            user_permissions=permissions
        )

    @staticmethod
    def generate_custom_usergroup(permissions: TykUserGroupPermissions, name: str = "Custom User Group"):
        return TykUserGroupModel(
            name=name,
            user_permissions=permissions
        )