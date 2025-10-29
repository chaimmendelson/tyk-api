import asyncio
from loguru import logger
from ..repositories import (
    TykApisRepository,
    TykAssetsRepository,
    TykCertificatesRepository,
    TykKeysRepository,
    TykOrganizationsRepository,
    TykPoliciesRepository,
    TykWebHooksRepository,
    TykMasterUsersRepository,
)
from ..models import (
    TykOrganizationModel,
    CreateOrganizationRequest,
    CreateBasicUserRequest,
    DeleteOrganizationRequest,
    DeleteUserRequest,
)

from ..errors import TykAPIError, TykBadRequestError

from .users import UsersService
from .applications import ApplicationService
from .usergroups import UserGroupService


async def execute_or_raise(coro, error_message: str):
    """Execute an async operation and raise TykAPIError on failure."""
    try:
        await coro
    except Exception as e:
        logger.error(f"{error_message}: {e}")
        raise TykAPIError(error_message) from e


class OrganizationService:
    """Service class responsible for managing Tyk organizations and their resources."""

    # -----------------------------------------------------
    # Organization Management
    # -----------------------------------------------------

    @staticmethod
    async def get_repo() -> TykOrganizationsRepository:
        """Return a repository instance for organizations."""
        return await TykOrganizationsRepository.instance()

    @staticmethod
    async def create_organization(
        org: CreateOrganizationRequest,
    ) -> TykOrganizationModel:
        """Create a new organization, validating that its application exists first."""
        repo = await OrganizationService.get_repo()

        if org.app_name not in await ApplicationService.get_applications():
            raise TykBadRequestError(
                f"Application '{org.app_name}' does not exist. Cannot create organization."
            )

        organization = await repo.create_organization(org.generate_organization)
        logger.info(
            f"Created organization {organization.id} ({organization.owner_name})"
        )

        return organization

    @staticmethod
    async def delete_organization(org_info: DeleteOrganizationRequest) -> None:
        """Delete an organization and all related Tyk resources."""
        repo = await OrganizationService.get_repo()
        org = await repo.get_organization_by_name(
            app_name=org_info.app_name,
            org_name=org_info.org_name,
        )

        org_id = org.id

        # Grouped resource deletions (safe to parallelize)
        cleanup_tasks = [
            (
                TykAssetsRepository,
                "delete_all_assets",
                f"Failed to delete assets for organization {org_id}",
            ),
            (
                TykApisRepository,
                "delete_all_apis",
                f"Failed to delete APIs for organization {org_id}",
            ),
            (
                TykCertificatesRepository,
                "delete_all_certificates",
                f"Failed to delete certificates for organization {org_id}",
            ),
            (
                TykPoliciesRepository,
                "delete_all_policies",
                f"Failed to delete policies for organization {org_id}",
            ),
            (
                TykKeysRepository,
                "delete_all_keys",
                f"Failed to delete keys for organization {org_id}",
            ),
            (
                TykWebHooksRepository,
                "delete_all_webhooks",
                f"Failed to delete webhooks for organization {org_id}",
            ),
        ]

        await OrganizationService._run_cleanup_tasks(cleanup_tasks, org_id)

        await execute_or_raise(
            UserGroupService.delete_all_usergroups(org_id),
            f"Failed to delete user groups for organization {org_id}",
        )
        
        # Delete all users in the organization
        await OrganizationService._delete_org_users(org_id)

        # Finally, delete the organization itself
        await execute_or_raise(
            repo.delete_organization(org),
            f"Failed to delete organization {org_id}",
        )

        logger.info(f"Deleted organization {org_id} ({org.owner_name})")

    # -----------------------------------------------------
    # Bootstrap and Helpers
    # -----------------------------------------------------

    @staticmethod
    async def bootstrap_organization_resources(
        org: TykOrganizationModel,
        user_password: str,
    ) -> None:
        """Create initial resources and basic users for a new organization."""
        await (await TykMasterUsersRepository.instance()).bootstrap_org_admin(org.id)

        for username in {org.owner_name, org.owner_slug} - {None}:

            if not username or username.strip() == "":
                continue
            user = CreateBasicUserRequest(
                org_id=org.id, username=username, password=user_password
            )
            await UsersService.create_basic_user(user)

    # -----------------------------------------------------
    # Internal Helpers
    # -----------------------------------------------------

    @staticmethod
    async def _run_cleanup_tasks(tasks: list[tuple], org_id: str):
        """Run all cleanup operations concurrently with individual error isolation."""

        async def _run(repo_cls, method_name, error_message):
            repo = await repo_cls.instance(org_id=org_id)
            method = getattr(repo, method_name)
            await execute_or_raise(method(), error_message)

        await asyncio.gather(*(_run(*t) for t in tasks))

    @staticmethod
    async def _delete_org_users(org_id: str):
        """Delete all users belonging to an organization."""
        try:
            users = await UsersService.get_users(org_id)
            if not users:
                return
            await asyncio.gather(
                *(
                    UsersService.delete_user(
                        DeleteUserRequest(
                            org_id=org_id, username=u.email_address.split("@")[0]
                        )
                    )
                    for u in users
                )
            )
        except Exception as e:
            logger.error(f"Error deleting users for organization {org_id}: {e}")
            raise TykAPIError(
                f"Failed to delete users for organization {org_id}"
            ) from e
