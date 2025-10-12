from .master_users import TykMasterUsersRepository

from .vanila_tyk import (
    TykUsersRepository,
    TykOrganizationsRepository,
    TykUserGroupsRepository,
    TykPoliciesRepository,
    TykKeysRepository,
    TykCertificatesRepository,
    TykApisRepository,
    TykAssetsRepository,
    TykWebHooksRepository,
    get_tyk_repository as get_tyk_repository_by_access_key,
    R
)

__all__ = [
    "TykUsersRepository",
    "TykOrganizationsRepository",
    "TykUserGroupsRepository",
    "TykPoliciesRepository",
    "TykKeysRepository",
    "TykCertificatesRepository",
    "TykApisRepository",
    "TykAssetsRepository",
    "TykWebHooksRepository",

    "get_tyk_repository",

    "get_tyk_users_repository",
    "get_tyk_usergroups_repository",
    "get_tyk_policies_repository",
    "get_tyk_organizations_repository",
    "get_tyk_apis_repository",
    "get_tyk_assets_repository",
    "get_tyk_certificates_repository",
    "get_tyk_keys_repository",
    "get_tyk_webhooks_repository",

    "master_users_repo"
]

master_users_repo = TykMasterUsersRepository()

async def get_tyk_repository(repo_cls: type[R], org_id: str | None = None) -> R:

    if org_id:
        access_key = await master_users_repo.get_org_admin_api_key(org_id=org_id)
    else:
        access_key = await master_users_repo.get_access_key()

    if access_key is None:
        raise ValueError("Access key is not set")

    return get_tyk_repository_by_access_key(repo_cls=repo_cls, api_key=access_key)

# ----------------------------------------------------------------------
# Optional explicit accessors for autocompletion
# ----------------------------------------------------------------------
async def get_tyk_users_repository(org_id: str | None = None) -> TykUsersRepository:
    return await get_tyk_repository(TykUsersRepository, org_id=org_id)

async def get_tyk_usergroups_repository(org_id: str | None = None) -> TykUserGroupsRepository:
    return await get_tyk_repository(TykUserGroupsRepository, org_id=org_id)

async def get_tyk_policies_repository(org_id: str | None = None) -> TykPoliciesRepository:
    return await get_tyk_repository(TykPoliciesRepository, org_id=org_id)

async def get_tyk_organizations_repository() -> TykOrganizationsRepository:
    return await get_tyk_repository(TykOrganizationsRepository)

async def get_tyk_apis_repository(org_id: str | None = None) -> TykApisRepository:
    return await get_tyk_repository(TykApisRepository, org_id=org_id)

async def get_tyk_assets_repository(org_id: str | None = None) -> TykAssetsRepository:
    return await get_tyk_repository(TykAssetsRepository, org_id=org_id)

async def get_tyk_certificates_repository(org_id: str | None = None) -> TykCertificatesRepository:
    return await get_tyk_repository(TykCertificatesRepository, org_id=org_id)

async def get_tyk_keys_repository(org_id: str | None = None) -> TykKeysRepository:
    return await get_tyk_repository(TykKeysRepository, org_id=org_id)

async def get_tyk_webhooks_repository(org_id: str | None = None) -> TykWebHooksRepository:
    return await get_tyk_repository(TykWebHooksRepository, org_id=org_id)
