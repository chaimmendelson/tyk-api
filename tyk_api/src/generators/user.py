from pydantic import EmailStr
from tyk_api.src.models import (
    TykUserModel,
    TykUserAdminPermissions,
    TykUserPermissionsModel,
    TykPermissionLevel,
)


class TykUserGenerator:
    """Generates TykUserModel instances for various roles."""

    @staticmethod
    def _extract_first_name(email_address: EmailStr) -> str:
        return str(email_address).split("@")[0].capitalize()

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
    def generate_super_admin_user(email_address: EmailStr, password: str | None = None) -> TykUserModel:
        return TykUserModel(
            first_name=TykUserGenerator._extract_first_name(email_address),
            last_name="SuperAdmin",
            email_address=email_address,
            password=password,
            user_permissions=TykUserGenerator._admin_permissions(),
        )

    @staticmethod
    def generate_org_admin_user(org_id: str, email_address: EmailStr, password: str | None = None) -> TykUserModel:
        return TykUserModel(
            first_name=TykUserGenerator._extract_first_name(email_address),
            last_name="Admin",
            email_address=email_address,
            password=password,
            user_permissions=TykUserGenerator._admin_permissions(),
            org_id=org_id,
        )

    @staticmethod
    def generate_basic_user(org_id: str, group_id: str, email_address: EmailStr, password: str | None = None) -> TykUserModel:
        return TykUserModel(
            first_name=TykUserGenerator._extract_first_name(email_address),
            last_name="User",
            email_address=email_address,
            password=password,
            user_permissions=TykUserGenerator._empty_permissions(),
            org_id=org_id,
            group_id=group_id,
        )

    @staticmethod
    def generate_gateway_user(org_id: str, group_id: str, email_address: EmailStr) -> TykUserModel:
        return TykUserModel(
            first_name=TykUserGenerator._extract_first_name(email_address),
            last_name="User",
            email_address=email_address,
            user_permissions=TykUserGenerator._empty_permissions(),
            org_id=org_id,
            group_id=group_id,
        )
