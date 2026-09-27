from pydantic import BaseModel, Field
from ..tyk import TykOrganizationUpdateModel, TykOrganizationCreateModel, TykOrganizationModel
from .application import ApplicationSlim

def to_tyk_name(app, org) -> str:

    if app == org:
        return app

    prefix = app + "-"

    if org.startswith(prefix):
        suffix = org.removeprefix(prefix)  # strip "app-"
        return f"{suffix}.{app}"

    # Case 2: org does NOT start with app → org.app
    return f"{org}.{app}"

def from_tyk_name(org) -> str:

    return org.replace(".", "-")

class Organization(ApplicationSlim):

    organization_name: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9]+((-[a-zA-Z0-9]+)?)*$",
        max_length=15,
    )

    @property
    def tyk_name(self) -> str:
        return to_tyk_name(self.application_name, self.organization_name)

    @classmethod
    def from_tyk_model(cls, tyk_model: TykOrganizationModel) -> "Organization":
        org_name = tyk_model.owner_name
        return cls(
            name=org_name,
            app=Application(tyk_model.owner_slug)
        )

    @property
    def create_model(self) -> TykOrganizationCreateModel:
        return TykOrganizationCreateModel(
            owner_name=self.tyk_name,
            owner_slug=self.app.name
        )

