from pydantic import EmailStr

from src.models import TykUserModel, TykUserAdminPermissions, TykUserPermissionsModel

class TykUserGenerator:

    @staticmethod
    def generate_org_admin_user(
        password: str,
        org_id: str,
        email_address: EmailStr,
        first_name: str = "Admin",
        last_name: str = "User",
    ):
        return TykUserModel(
            first_name=first_name,
            last_name=last_name,
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
        password: str,
        email_address: EmailStr,
        first_name: str = "Super",
        last_name: str = "Admin",
    ):
        return TykUserModel(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            password=password,
            user_permissions=TykUserPermissionsModel(
                IsAdmin=TykUserAdminPermissions.ADMIN,
                ResetPassword=TykUserAdminPermissions.ADMIN
            ),
        )

    @staticmethod
    def generate_regular_user(
        password: str,
        org_id: str,
        group_id: str,
        email_address: EmailStr,
        first_name: str,
        last_name: str = "User",

    ):
        return TykUserModel(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            password=password,
            user_permissions=TykUserPermissionsModel(),
            org_id=org_id,
            group_id=group_id
        )

