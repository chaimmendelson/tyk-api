from pydantic import BaseModel
from ...models import TykOrganizationCreateModel
from ...generators import TykOrganizationGenerator

class CreateOrganizationRequest(BaseModel):
    app_name: str
    org_name: str
    
    
    @property
    def generate_organization(self) -> TykOrganizationCreateModel:
        
        organization = TykOrganizationGenerator.generate_from_application(
            application=self.app_name,
            name=self.org_name,
        )

        return organization

class DeleteOrganizationRequest(BaseModel):
    app_name: str
    org_name: str