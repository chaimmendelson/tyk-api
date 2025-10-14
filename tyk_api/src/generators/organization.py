from tyk_api.src.models import TykOrganizationModel
from tyk_api.src.helpers.syntax import concat_application_organization, validate_application_name, validate_organization_name

class TykOrganizationGenerator:
    @staticmethod
    def generate(
        owner_name: str,
        owner_slug: str,
        cname: str | None = None,
    ) -> TykOrganizationModel:
        owner_name = owner_name.lower().strip()
        owner_slug = owner_slug.lower().strip()
        cname = cname.lower().strip() if cname else None
        
        org = TykOrganizationModel(
            owner_name=owner_name,
            owner_slug=owner_slug,
        )
        
        if cname:
            org.cname = cname
            org.cname_enabled = True

        return org
    
    @staticmethod
    def generate_from_application(application: str, name: str) -> TykOrganizationModel:
        owner_slug = validate_application_name(application)
        owner_name = concat_application_organization(application, name)
        cname = owner_name

        return TykOrganizationGenerator.generate(
            owner_name=owner_name,
            owner_slug=owner_slug,
            cname=cname,
        )