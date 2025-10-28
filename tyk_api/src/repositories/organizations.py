from typing import List

from tyk_api.src.api import TykOrganizationsApi
from tyk_api.src.models import (
    TykOrganizationModel,
    TykOrganizationCreateModel,
    TykOrganizationUpdateModel,
)
from tyk_api.src.errors import (
    TykNameConflictError,
    TykAPIError,
    TykNotFoundError,
    TykBadRequestError,
)
from ..generators import TykOrganizationGenerator
from ..helpers import syntax
from .base import TykAdminRepository

RESOURCE_NAME = "Organization"


class TykOrganizationsRepository(TykAdminRepository[TykOrganizationsApi]):
    """Repository for managing Tyk organizations through the Admin API."""

    api_cls = TykOrganizationsApi

    def __init__(self, api: TykOrganizationsApi):
        super().__init__(api)

    # ──────────────────────────────── CREATE ────────────────────────────────

    async def create_organization(self, org: TykOrganizationCreateModel) -> TykOrganizationModel:
        """Internal helper to create an organization, ensuring uniqueness and validation."""
        if not org.owner_name or not org.owner_name.strip():
            raise TykBadRequestError("Organization owner name cannot be empty.")

        try:
            existing_org = await self.get_organization_by_owner_name(org.owner_name)
            
            if existing_org:
                raise TykNameConflictError(RESOURCE_NAME, org.owner_name)
        except TykNotFoundError:
            # Ignore lookup errors (e.g., org not found)
            pass

        return await self.api.create_organization(org)

    # ──────────────────────────────── READ ────────────────────────────────

    async def get_organizations(self) -> list[TykOrganizationModel]:
        return await self.api.get_organizations()

    async def get_organization_by_id(self, org_id: str) -> TykOrganizationModel | None:
        return await self.api.get_organization(org_id)

    async def get_organization_by_owner_name(self, owner_name: str) -> TykOrganizationModel:
        orgs = await self.get_organizations()
        for org in orgs:
            if org.owner_name == owner_name:
                return org
        raise TykNotFoundError(RESOURCE_NAME, f"{owner_name=}")

    async def get_organizations_by_owner_slug(self, owner_slug: str) -> List[TykOrganizationModel]:
        orgs = await self.get_organizations()
        return [org for org in orgs if org.owner_slug == owner_slug]

    async def get_organization_by_cname(self, cname: str) -> TykOrganizationModel:
        orgs = await self.get_organizations()
        for org in orgs:
            if org.cname == cname:
                return org
        raise TykNotFoundError(RESOURCE_NAME, f"{cname=}")

    async def get_organizations_by_application(self, app_name: str) -> list[TykOrganizationModel]:
        return await self.get_organizations_by_owner_slug(app_name)

    async def get_organization_by_name(self, app_name: str, org_name: str) -> TykOrganizationModel:
        name = syntax.concat_application_organization(app_name, org_name)
        return await self.get_organization_by_owner_name(name)

    # ──────────────────────────────── UPDATE & DELETE ────────────────────────────────

    async def update_organization(self, org: TykOrganizationUpdateModel) -> TykOrganizationModel:
        return await self.api.update_organization(org)

    async def delete_organization(self, org: TykOrganizationModel) -> None:
        await self.api.delete_organization(org)
