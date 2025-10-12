from horizon_fastapi_template.utils import BaseAPI

from .apis import TykApisRepository
from .assets import TykAssetsRepository
from .certificates import TykCertificatesRepository
from .keys import TykKeysRepository
from .organizations import TykOrganizationsRepository
from .policies import TykPoliciesRepository
from .usergroups import TykUserGroupsRepository
from .users import TykUsersRepository
from .webhooks import TykWebHooksRepository

from .master_users import TykMasterUsersRepository

from src.api import *

from src.settings import settings

tyk_admin_api = BaseAPI(
    base_url=settings.DASHBOARD_URL,
    headers={
        "admin-auth": settings.ADMIN_AUTH
    },
)

tyk_master_users_repository = TykMasterUsersRepository(TykUsersAdminApi(tyk_admin_api))

def get_tyk_api(api_key: str) -> BaseAPI:
    return BaseAPI(
        base_url=settings.DASHBOARD_URL,
        headers={
            "Authorization": api_key,
        },
    )


async def get_access_key(org_id: str | None = None) -> str | None:
    
    access_key = await tyk_master_users_repository.get_access_key()
    
    if org_id:
        access_key = await tyk_master_users_repository.get_org_admin_api_key(org_id)

    if not access_key:
        raise ValueError("No access key available")

    return access_key

async def get_users_repository(org_id: str | None = None) -> TykUsersRepository:
    access_key = await get_access_key(org_id) or ""
    
    users_api = TykUsersApi(get_tyk_api(access_key))
    
    admin_users_api = TykUsersAdminApi(tyk_admin_api)
    
    return TykUsersRepository(
        api=users_api,
        admin_api=admin_users_api
    )

def get_organizations_repository() -> TykOrganizationsRepository:
    
    org_api = TykOrganizationsApi(tyk_admin_api)
    
    return TykOrganizationsRepository(org_api)

async def get_usergroups_repository(org_id: str | None = None) -> TykUserGroupsRepository:
    access_key = await get_access_key(org_id) or ""
    
    usergroup_api = TykUserGroupsAPI(get_tyk_api(access_key))
    
    return TykUserGroupsRepository(usergroup_api)

async def get_policies_repository(org_id: str | None = None) -> TykPoliciesRepository:
    access_key = await get_access_key(org_id) or ""
    
    policies_api = TykPoliciesApi(get_tyk_api(access_key))
    
    return TykPoliciesRepository(policies_api)

async def get_keys_repository(org_id: str | None = None) -> TykKeysRepository:
    access_key = await get_access_key(org_id) or ""
    
    keys_api = TykKeysApi(get_tyk_api(access_key))
    
    return TykKeysRepository(keys_api)

async def get_certificates_repository(org_id: str | None = None) -> TykCertificatesRepository:
    access_key = await get_access_key(org_id) or ""
    
    certificates_api = TykCertificatesApi(get_tyk_api(access_key))
    
    return TykCertificatesRepository(certificates_api)

async def get_apis_repository(org_id: str | None = None) -> TykApisRepository:
    access_key = await get_access_key(org_id) or ""
    
    apis_api = TykApisApi(get_tyk_api(access_key))
    
    return TykApisRepository(apis_api)

async def get_assets_repository(org_id: str | None = None) -> TykAssetsRepository:
    access_key = await get_access_key(org_id) or ""
    
    assets_api = TykAssetsApi(get_tyk_api(access_key))
    
    return TykAssetsRepository(assets_api)

async def get_webhooks_repository(org_id: str | None = None) -> TykWebHooksRepository:
    access_key = await get_access_key(org_id) or ""
    
    webhooks_api = TykWebHooksApi(get_tyk_api(access_key))
    
    return TykWebHooksRepository(webhooks_api)