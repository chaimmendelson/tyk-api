from ..repositories import (
    TykApisRepository,
    TykAssetsRepository,
    TykCertificatesRepository,
    TykKeysRepository,
    TykOrganizationsRepository,
    TykPoliciesRepository,
    TykUsersRepository,
    TykUserGroupsRepository,
    TykWebHooksRepository,
    TykMasterUsersRepository,
    TykApplicationsRepository,
)

from ..models import TykOrganizationModel, CreateOrganizationRequest, CreateBasicUserRequest
from ..generators import TykUserGenerator
from ..errors import TykAPIError, TykBadRequestError
from loguru import logger

class OrganizationService:

    @staticmethod
    async def get_repo() -> TykOrganizationsRepository:
        return await TykOrganizationsRepository.instance()

    @staticmethod
    async def bootstrap_organization_resources(org: TykOrganizationModel, user_password: str | None = None) -> None:

        await (await TykMasterUsersRepository.instance()).bootstrap_org_admin(org.id)

        users_repo = await TykUsersRepository.instance(org_id=org.id)

        if user_password:
            if org.owner_name:
                user = CreateBasicUserRequest(
                    org_id=org.id,
                    username=org.owner_name,
                    password=user_password,
                )
                await users_repo.create_user(
                    user=await user.generate_user,
                )
            if org.owner_slug and org.owner_slug != org.owner_name:
                
                user = CreateBasicUserRequest(
                    org_id=org.id,
                    username=org.owner_slug,
                    password=user_password,
                )
                
                await users_repo.create_user(
                    user=await user.generate_user,
                )

    @staticmethod
    async def create_organization(org: CreateOrganizationRequest) -> TykOrganizationModel:

        repo = await OrganizationService.get_repo()
        applications_repo = await TykApplicationsRepository.instance(admin=True)

        if not await applications_repo.application_usergroup_exists(org.app_name):
            raise TykBadRequestError(f"Application '{org.app_name}' does not exist. Cannot create organization.")

        organization = await repo.create_organization(org.generate_organization)

        logger.info(f"Created organization {organization.id} - {organization.owner_name}")
        
        return organization

    @staticmethod
    async def delete_organization(org: TykOrganizationModel) -> None:

        repo = await OrganizationService.get_repo()

        if not org.id:
            raise TykAPIError("Organization ID is not set, cannot delete organization.")
        
        try:
            await (await TykAssetsRepository.instance(org_id=org.id)).delete_all_assets()
        except Exception as e:
            logger.error(f"Error deleting assets for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete assets for organization {org.id}")
        
        try:
            apis_repo = await TykApisRepository.instance(org_id=org.id)
            await apis_repo.delete_all_apis()
        except Exception as e:
            logger.error(f"Error deleting APIs for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete APIs for organization {org.id}")
        
        try:
            certificates_repo = await TykCertificatesRepository.instance(org_id=org.id)
            await certificates_repo.delete_all_certificates()
        except Exception as e:
            logger.error(f"Error deleting certificates for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete certificates for organization {org.id}")
        
        try:
            policies_repo = await TykPoliciesRepository.instance(org_id=org.id)
            await policies_repo.delete_all_policies()
        except Exception as e:
            logger.error(f"Error deleting policies for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete policies for organization {org.id}")
        
        try:
            usergroups_repo = await TykUserGroupsRepository.instance(org_id=org.id)
            usergroups = await usergroups_repo.get_usergroups()
            for usergroup in usergroups or []:
                await usergroups_repo.delete_usergroup(usergroup)
        except Exception as e:
            logger.error(f"Error deleting user groups for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete user groups for organization {org.id}")

        try:
            keys_repo = await TykKeysRepository.instance(org_id=org.id)
            await keys_repo.delete_all_keys()
        except Exception as e:
            logger.error(f"Error deleting keys for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete keys for organization {org.id}")


        try:
            webhooks_repo = await TykWebHooksRepository.instance(org_id=org.id)
            await webhooks_repo.delete_all_webhooks()
        except Exception as e:
            logger.error(f"Error deleting webhooks for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete webhooks for organization {org.id}")

        try:
            users_repo = await TykUsersRepository.instance(admin=True)
            users = await users_repo.get_users_by_organization(org.id)
            for user in users or []:
                await users_repo.delete_user(user)
        except Exception as e:
            logger.error(f"Error deleting users for organization {org.id}: {e}")
            raise TykAPIError(f"Failed to delete users for organization {org.id}")
        
        try:
            await repo.delete_organization(org)
            logger.info(f"Deleted organization {org.id} - {org.owner_name}")
        except Exception as e:
            logger.error(f"Error deleting organization: {e}")
            raise TykAPIError(f"Failed to delete organization {org.id}")