from pydantic import EmailStr
from tyk_api.src.models import (
    TykUserModel,
    TykUserAdminPermissions,
    TykUserPermissionsModel,
    TykPermissionLevel,
    MainUserTypes
)
from tyk_api.src.settings import settings


class TykUserGenerator:
    """Generates TykUserModel instances for various roles."""

    @staticmethod
    def _create_email(username: str) -> EmailStr:
        return f"{username}@{settings.EMAIL_DOMAIN}"

    @staticmethod
    def _admin_permissions() -> TykUserPermissionsModel:
        return TykUserPermissionsModel(
            IsAdmin=TykUserAdminPermissions.ADMIN,
            ResetPassword=TykUserAdminPermissions.ADMIN,
        )

    @staticmethod
    def _empty_permissions() -> TykUserPermissionsModel:
        return TykUserPermissionsModel(system=TykPermissionLevel.DENY)

    @staticmethod
    def generate_super_admin_user(username: str, password: str | None = None) -> TykUserModel:
        return TykUserModel(
            first_name=username.capitalize(),
            last_name="SuperAdmin",
            email_address=TykUserGenerator._create_email(username),
            password=password,
            user_permissions=TykUserGenerator._admin_permissions(),
        )

    @staticmethod
    def generate_org_admin_user(org_id: str, username: str, password: str | None = None) -> TykUserModel:
        return TykUserModel(
            first_name=username.capitalize(),
            last_name="Admin",
            email_address=TykUserGenerator._create_email(username),
            password=password,
            user_permissions=TykUserGenerator._admin_permissions(),
            org_id=org_id,
        )

    @staticmethod
    def generate_basic_user(org_id: str, group_id: str, username: str, password: str | None = None) -> TykUserModel:
        return TykUserModel(
            first_name=username.capitalize(),
            last_name="User",
            email_address=TykUserGenerator._create_email(username),
            password=password,
            user_permissions=TykUserGenerator._empty_permissions(),
            org_id=org_id,
            group_id=group_id,
        )

    @staticmethod
    def generate_gateway_user(org_id: str, group_id: str, username: str) -> TykUserModel:
        return TykUserModel(
            first_name=username.capitalize(),
            last_name="User",
            email_address=TykUserGenerator._create_email(username),
            user_permissions=TykUserGenerator._empty_permissions(),
            org_id=org_id,
            group_id=group_id,
        )
        
    @staticmethod
    def generate_clean_user(username: str, org_id: str | None = None, password: str | None = None) -> TykUserModel:
        return TykUserModel(
            first_name=username.capitalize(),
            last_name="User",
            email_address=TykUserGenerator._create_email(username),
            user_permissions=TykUserGenerator._empty_permissions(),
            org_id=org_id,
            password=password,
        )
        
    @staticmethod
    def generate(user_type: MainUserTypes, org_id: str | None, group_id: str | None, username: str, password: str | None = None) -> TykUserModel:

        if user_type == MainUserTypes.SUPER_ADMIN:
            return TykUserGenerator.generate_super_admin_user(username, password)

        elif user_type == MainUserTypes.ORG_ADMIN:
            if org_id is None:
                raise ValueError("org_id is required for org_admin users.")
            return TykUserGenerator.generate_org_admin_user(org_id, username, password)

        elif user_type == MainUserTypes.BASIC_USER:
            if org_id is None or group_id is None:
                raise ValueError("org_id and group_id are required for basic_user users.")
            return TykUserGenerator.generate_basic_user(org_id, group_id, username, password)

        elif user_type == MainUserTypes.GATEWAY_USER:
            if org_id is None or group_id is None:
                raise ValueError("org_id and group_id are required for gateway_user users.")
            return TykUserGenerator.generate_gateway_user(org_id, group_id, username)
        
        else:
            raise ValueError(f"Unknown user type: {user_type}")
        
    @staticmethod
    def convert_existing_user(user_type: MainUserTypes, user: TykUserModel) -> TykUserModel:
        if user_type == MainUserTypes.SUPER_ADMIN:
            user.user_permissions = TykUserGenerator._admin_permissions()
            user.org_id = None
            user.group_id = None
            return user

        elif user_type == MainUserTypes.ORG_ADMIN:
            user.user_permissions = TykUserGenerator._admin_permissions()
            user.group_id = None
            return user

        elif user_type == MainUserTypes.BASIC_USER:
            user.user_permissions = TykUserGenerator._empty_permissions()
            return user

        elif user_type == MainUserTypes.GATEWAY_USER:
            user.user_permissions = TykUserGenerator._empty_permissions()
            user.password = None  # Gateway users do not have passwords
            return user
        
        else:
            raise ValueError(f"Unknown user type: {user_type}")
