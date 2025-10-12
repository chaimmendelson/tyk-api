from ..base import BaseAPI, TykApi
from src.models import TykOrganizationModel

ORGANIZATIONS_KEY = "organisations"

class TykOrganizationsApi(TykApi):
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/admin/organisations",
    ):
        super().__init__(api, base_uri)

    async def get_organizations(self) -> list[TykOrganizationModel]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()

        organizations_data = response.json().get(ORGANIZATIONS_KEY, []) or []

        return [TykOrganizationModel.model_validate(org) for org in organizations_data]

    async def get_organization(self, org_id: str) -> TykOrganizationModel:
        response = await self.api.client.get(f"{self.base_uri}/{org_id}")

        response.raise_for_status()

        return TykOrganizationModel.model_validate(response.json())

    async def create_organization(self, org: TykOrganizationModel) -> TykOrganizationModel:
        response = await self.api.client.post(self.base_uri, json=org.model_dump())

        response.raise_for_status()
        
        org_id = response.json().get("Meta")
        
        if org_id is None:
            raise ValueError("Failed to create organization: Missing Meta field in response")

        org.id = org_id

        return org

    async def update_organization(self, org: TykOrganizationModel) -> TykOrganizationModel:
        response = await self.api.client.put(f"{self.base_uri}/{org.id}", json=org.model_dump())

        response.raise_for_status()

        return TykOrganizationModel.model_validate(response.json())

    async def delete_organization(self, org: TykOrganizationModel):
        response = await self.api.client.delete(f"{self.base_uri}/{org.id}")

        response.raise_for_status()