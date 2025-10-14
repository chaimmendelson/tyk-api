from typing import List
from tyk_api.src.api import TykOrganizationsApi
from tyk_api.src.models import TykOrganizationModel
from .base import TykAdminRepository
from tyk_api.src.errors import TykNameConflictError

class TykOrganizationsRepository(TykAdminRepository[TykOrganizationsApi]):

    api_cls = TykOrganizationsApi
    
    def __init__(self, api: TykOrganizationsApi):
        super().__init__(api)

    async def create_organization(self, org: TykOrganizationModel) -> TykOrganizationModel:
        existing_orgs = await self.get_organizations_by_owner_name(org.owner_name or "")

        if existing_orgs:
            raise TykNameConflictError("organization", org.owner_name or "")
        
        return await self.api.create_organization(org)
    
    async def get_organizations(self) -> list[TykOrganizationModel]:
        return await self.api.get_organizations()
    
    async def get_organization_by_id(self, org_id: str) -> TykOrganizationModel | None:
        return await self.api.get_organization(org_id)

    async def get_organizations_by_owner_name(self, owner_name: str) -> List[TykOrganizationModel]:

        orgs = await self.get_organizations()
        return [org for org in orgs if org.owner_name == owner_name]

    async def get_organizations_by_owner_slug(self, owner_slug: str) -> List[TykOrganizationModel]:

        orgs = await self.get_organizations()
        return [org for org in orgs if org.owner_slug == owner_slug]

    async def get_organizations_by_cname(self, cname: str) -> List[TykOrganizationModel]:

        orgs = await self.get_organizations()

        return [org for org in orgs if org.cname == cname]

    async def update_organization(self, org: TykOrganizationModel) -> TykOrganizationModel:
        return await self.api.update_organization(org)
    
    async def delete_organization(self, org: TykOrganizationModel) -> None:
        await self.api.delete_organization(org)