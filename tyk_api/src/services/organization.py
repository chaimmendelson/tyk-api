from ..repositories import (
    get_tyk_organizations_repository,
    TykOrganizationsRepository,
    master_users_repo,
    
    get_tyk_apis_repository,
    get_tyk_assets_repository,
    get_tyk_certificates_repository,
    get_tyk_policies_repository,
    get_tyk_keys_repository,
    get_tyk_webhooks_repository,
    get_tyk_users_repository,
    get_tyk_usergroups_repository,
)

from ..settings import settings
from ..models import TykOrganizationModel, MainUserTypes
from ..generators import TykOrganizationGenerator, TykUserGenerator
from ..errors import TykAPIError, TykNameConflictError
from loguru import logger

from .basic_users import BasicUsersService

class OrganizationService:
    
    def __init__(self):
        self.repo: TykOrganizationsRepository | None = None

    async def _initialize_repo(self) -> None:
        if not self.repo:
            self.repo = await get_tyk_organizations_repository()

    async def _bottstrap_organization_resources(self, org: TykOrganizationModel, user_password: str | None = None) -> None:
        if not org.id:
            raise TykAPIError("Organization ID is not set, cannot bootstrap resources.")

        await master_users_repo.bootstrap_org_admin(org.id)
        
        users_service = BasicUsersService()
        
        await users_service._initialize_repo()

        await users_service.create_main_gateway_user(org)
        
        if user_password:
            if org.owner_name:
                await users_service.create_user(
                    user_type=MainUserTypes.BASIC_USER,
                    user=TykUserGenerator.generate_clean_user(org.owner_name, org.id, password=user_password),
                )
            if org.owner_slug and org.owner_slug != org.owner_name:
                await users_service.create_user(
                    user_type=MainUserTypes.BASIC_USER,
                    user=TykUserGenerator.generate_clean_user(org.owner_slug, org.id, password=user_password),
                )

    async def create_organization(self, app_name: str, org_name: str, user_password: str | None = None) -> TykOrganizationModel:
        await self._initialize_repo()
        
        if not self.repo:
            raise TykAPIError("Organizations repository not initialized.")

        org_model = TykOrganizationGenerator.generate_from_application(app_name, org_name)
        
        try:
            org_model = await self.repo.create_organization(org_model)
            logger.info(f"Created organization {org_model.id} - {org_model.owner_name}")
            await self._bottstrap_organization_resources(org_model, user_password=user_password)
            return org_model
        except TykNameConflictError as e:
            logger.error(f"Organization with owner name '{org_model.owner_name}' already exists.")
            raise e
        except Exception as e:
            logger.error(f"Error creating organization: {e}")
            
            if org_model.id:
                await self.delete_organization(org_model)
                
            raise TykAPIError("Failed to create organization and bootstrap resources.")
    
    async def get_organization(self, org_id: str) -> TykOrganizationModel | None:
        await self._initialize_repo()
        
        if not self.repo:
            raise TykAPIError("Organizations repository not initialized.")
        
        return await self.repo.get_organization_by_id(org_id)
    
    async def delete_organization(self, org: TykOrganizationModel) -> None:
        if not self.repo:
            raise TykAPIError("Organizations repository not initialized.")
        
        if not org.id:
            raise TykAPIError("Organization ID is not set, cannot delete organization.")
        
        try:
            assets_repo = await get_tyk_assets_repository(org.id)
            assets = await assets_repo.get_assets()
            for asset in assets or []:
                await assets_repo.delete_asset(asset)
        except Exception as e:
            logger.error(f"Error deleting assets for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete assets for organization {org.id}")
        
        try:
            apis_repo = await get_tyk_apis_repository(org.id)
            apis = await apis_repo.get_apis()
            for api in apis or []:
                await apis_repo.delete_api(api)
        except Exception as e:
            logger.error(f"Error deleting APIs for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete APIs for organization {org.id}")
        
        try:
            certificates_repo = await get_tyk_certificates_repository(org.id)
            certificates = await certificates_repo.get_certificates()
            for cert in certificates or []:
                await certificates_repo.delete_certificate(cert)
        except Exception as e:
            logger.error(f"Error deleting certificates for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete certificates for organization {org.id}")
        
        try:
            policies_repo = await get_tyk_policies_repository(org.id)
            policies = await policies_repo.get_policies()
            for policy in policies or []:
                await policies_repo.delete_policy(policy)
        except Exception as e:
            logger.error(f"Error deleting policies for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete policies for organization {org.id}")
        
        try:
            usergroups_repo = await get_tyk_usergroups_repository(org.id)
            usergroups = await usergroups_repo.get_usergroups()
            for usergroup in usergroups or []:
                await usergroups_repo.delete_usergroup(usergroup)
        except Exception as e:
            logger.error(f"Error deleting user groups for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete user groups for organization {org.id}")

        try:
            keys_repo = await get_tyk_keys_repository(org.id)
            keys = await keys_repo.get_keys(org_id=org.id)
            for key in keys or []:
                await keys_repo.delete_key(key)
        except Exception as e:
            logger.error(f"Error deleting keys for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete keys for organization {org.id}")


        try:
            webhooks_repo = await get_tyk_webhooks_repository(org.id)
            webhooks = await webhooks_repo.get_webhooks()
            for webhook in webhooks or []:
                await webhooks_repo.delete_webhook(webhook)
        except Exception as e:
            logger.error(f"Error deleting webhooks for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete webhooks for organization {org.id}")

        try:
            users_repo = await get_tyk_users_repository()
            users = await users_repo.get_users_by_organization(org.id)
            for user in users or []:
                await users_repo.delete_user(user)
        except Exception as e:
            logger.error(f"Error deleting users for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete users for organization {org.id}")
        
        try:
            await self.repo.delete_organization(org)
            logger.info(f"Deleted organization {org.id} - {org.owner_name}")
        except Exception as e:
            logger.error(f"Error deleting organization: {e}")
            raise TykAPIError(f"Failed to delete organization {org.id}")