from pydantic import EmailStr

from src.models import TykUserModel, TykUserAdminPermissions, TykUserPermissionsModel, TykPermissionLevel

class TykUserGenerator:

    @staticmethod
    def generate_org_admin_user(
        org_id: str,
        email_address: EmailStr,
        password: str | None = None,
    ):
        return TykUserModel(
            first_name=email_address.split("@")[0].capitalize(),
            last_name="Admin",
            email_address=email_address,
            password=password,
            user_permissions=TykUserPermissionsModel(
                IsAdmin=TykUserAdminPermissions.ADMIN,
                ResetPassword=TykUserAdminPermissions.ADMIN
            ),
            org_id=org_id
        )

    @staticmethod
    def generate_super_admin_user(
        email_address: EmailStr,
        password: str | None = None,
    ):
        return TykUserModel(
            first_name=email_address.split("@")[0].capitalize(),
            last_name="SuperAdmin",
            email_address=email_address,
            password=password,
            user_permissions=TykUserPermissionsModel(
                IsAdmin=TykUserAdminPermissions.ADMIN,
                ResetPassword=TykUserAdminPermissions.ADMIN
            ),
        )

    @staticmethod
    def generate_regular_user(
        org_id: str,
        group_id: str,
        email_address: EmailStr,
        password: str | None = None

    ):
        return TykUserModel(
            first_name=email_address.split("@")[0].capitalize(),
            last_name="User",
            email_address=email_address,
            password=password,
            user_permissions=TykUserPermissionsModel(
                system=TykPermissionLevel.DENY
            ),
            org_id=org_id,
            group_id=group_id
        )

    @staticmethod
    def generate_gateway_user(
        org_id: str,
        group_id: str,
        email_address: EmailStr,
    ):
        return TykUserModel(
            first_name=email_address.split("@")[0].capitalize(),
            last_name="User",
            email_address=email_address,
            user_permissions=TykUserPermissionsModel(
                system=TykPermissionLevel.DENY
            ),
            org_id=org_id,
            group_id=group_id
        )
