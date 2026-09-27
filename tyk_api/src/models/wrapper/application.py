import json

from pydantic import BaseModel, Field

from .. import TykUserGroupPermissions, TykPermissionLevel, TykUserGroupCreateModel, TykUserGroupUpdateModel
from ..tyk import TykUserGroupModel
from ...helpers import password_cipher

APPLICATION_PREFIX = "application-user-group-"

class ApplicationSlim(BaseModel):

    application_name: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9]+((-[a-zA-Z0-9]+)?)*$",
        max_length=15,
    )

    @classmethod
    def from_user_group(cls, user_group: TykUserGroupModel) -> "ApplicationSlim":
        if not user_group.name.startswith(APPLICATION_PREFIX):
            raise ValueError("User group name does not start with the application prefix")

        application_name = user_group.name.removeprefix(APPLICATION_PREFIX)

        return cls(
            application_name=application_name,
        )

class Application(ApplicationSlim):

    application_password: str = Field(
        ...,
        min_length=8,
    )

    @property
    def application_slim(self) -> ApplicationSlim:
        return ApplicationSlim(
            application_name=self.application_name,
        )

    @property
    def tyk_create_model(self) -> TykUserGroupCreateModel:
        return TykUserGroupCreateModel(
            name=f"{APPLICATION_PREFIX}{self.application_name}",
            user_permissions=TykUserGroupPermissions(system=TykPermissionLevel.DENY),
            description=json.dumps({
                "application_password": password_cipher.encrypt(self.application_password)
            })
        )

    @classmethod
    def from_user_group(cls, user_group: TykUserGroupModel) -> "Application":
        if not user_group.name.startswith(APPLICATION_PREFIX):
            raise ValueError("User group name does not start with the application prefix")

        application_name = user_group.name.removeprefix(APPLICATION_PREFIX)

        password = json.loads(user_group.description or "{}").get("application_password")

        if not password:
            raise ValueError("Application password not found in user group description")

        return cls(
            application_name=application_name,
            application_password=password_cipher.decrypt(password),
        )

    def generate_update(self, existing_usergroup: TykUserGroupModel) -> TykUserGroupUpdateModel:
        model = existing_usergroup.update_model

        model.name = f"{APPLICATION_PREFIX}{self.application_name}"

        model.description = json.dumps({
            "application_password": password_cipher.encrypt(self.application_password)
        })

        return model