from src.api import TykOrganizationsApi
from src.models import TykOrganizationModel
from .base import TykRepository

class TykOrganizationsRepository(TykRepository):

    def __init__(self, api: TykOrganizationsApi):
        super().__init__(api)
        self.api = api
    
    async def create_organization(self, org: TykOrganizationModel) -> TykOrganizationModel:
        return await self.api.create_organization(org)
    
    async def get_organizations(self) -> list[TykOrganizationModel]:
        return await self.api.get_organizations()
    
    async def get_organization_by_id(self, org_id: str) -> TykOrganizationModel | None:
        return await self.api.get_organization(org_id)
    
    async def get_organization_by_owner_name(self, owner_name: str) -> TykOrganizationModel | None:
        
        orgs = await self.get_organizations()
        
        for org in orgs:
            if org.owner_name == owner_name:
                return org
        
        return None

    async def get_organization_by_owner_slug(self, owner_slug: str) -> TykOrganizationModel | None:

        orgs = await self.get_organizations()

        for org in orgs:
            if org.owner_slug == owner_slug:
                return org

        return None

    async def get_organization_by_cname(self, cname: str) -> TykOrganizationModel | None:

        orgs = await self.get_organizations()

        for org in orgs:
            if org.cname == cname:
                return org

        return None

    async def update_organization(self, org: TykOrganizationModel) -> TykOrganizationModel:
        return await self.api.update_organization(org)
    
    async def delete_organization(self, org: TykOrganizationModel) -> None:
        await self.api.delete_organization(org)