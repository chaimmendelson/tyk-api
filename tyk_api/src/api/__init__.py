from typing import Type, TypeVar
from horizon_fastapi_template.utils import BaseAPI
from tyk_api.src.settings import settings

from .base import (
    TykApi,
    TykDashboardApi,
    TykDashboardAdminApi,
)
from .dashboard import (
    TykUsersApi,
    TykUserGroupsAPI,
    TykApisApi,
    TykAssetsApi,
    TykPoliciesApi,
    TykCertificatesApi,
    TykIdentityManagementProfilesAPI,
    TykKeysApi,
    TykWebHooksApi,
)
from .dashboard_admin import (
    TykUsersAdminApi,
    TykOrganizationsApi,
)

__all__ = [
    "get_tyk_api",

    "get_tyk_users_api",
    "get_tyk_usergroups_api",
    "get_tyk_apis_api",
    "get_tyk_assets_api",
    "get_tyk_policies_api",
    "get_tyk_certificates_api",
    "get_tyk_identity_management_profiles_api",
    "get_tyk_keys_api",
    "get_tyk_webhooks_api",
    "get_tyk_users_admin_api",
    "get_tyk_organizations_api",

    "TykApi",
    "TykDashboardApi",
    "TykDashboardAdminApi",
    "TykUsersApi",
    "TykUserGroupsAPI",
    "TykApisApi",
    "TykAssetsApi",
    "TykPoliciesApi",
    "TykCertificatesApi",
    "TykIdentityManagementProfilesAPI",
    "TykKeysApi",
    "TykWebHooksApi",
    "TykUsersAdminApi",
    "TykOrganizationsApi",
]

# ----------------------------------------------------------------------
# Type variable for all Tyk API subclasses
# ----------------------------------------------------------------------

T = TypeVar("T", bound=TykApi)

# ----------------------------------------------------------------------
# Base API builders
# ----------------------------------------------------------------------

def _build_base_api(
    api_key: str | None = None,
    admin: bool = False,
    override_base_url: str | None = None,
) -> BaseAPI:
    """Return a configured BaseAPI instance."""
    base_url = override_base_url or settings.DASHBOARD_URL
    headers = {"admin-auth": settings.ADMIN_AUTH} if admin else {"Authorization": api_key or ""}
    return BaseAPI(base_url=base_url, headers=headers)

# ----------------------------------------------------------------------
# Smart generic API factory
# ----------------------------------------------------------------------

def get_tyk_api(api_cls: Type[T], api_key: str | None = None, override_base_url: str | None = None) -> T:
    """
    Automatically choose admin or regular authentication
    based on whether the class inherits from TykDashboardAdminApi.
    """
    if issubclass(api_cls, TykDashboardAdminApi):
        base_api = _build_base_api(admin=True, override_base_url=override_base_url)
    else:
        if not api_key:
            raise ValueError(f"API key required for non-admin API: {api_cls.__name__}")
        base_api = _build_base_api(api_key=api_key, override_base_url=override_base_url)
    return api_cls(base_api)

# ----------------------------------------------------------------------
# Regular (user) API accessors
# ----------------------------------------------------------------------

def get_tyk_users_api(api_key: str, override_base_url: str | None = None) -> TykUsersApi:
    return get_tyk_api(TykUsersApi, api_key, override_base_url)

def get_tyk_usergroups_api(api_key: str, override_base_url: str | None = None) -> TykUserGroupsAPI:
    return get_tyk_api(TykUserGroupsAPI, api_key, override_base_url)

def get_tyk_apis_api(api_key: str, override_base_url: str | None = None) -> TykApisApi:
    return get_tyk_api(TykApisApi, api_key, override_base_url)

def get_tyk_assets_api(api_key: str, override_base_url: str | None = None) -> TykAssetsApi:
    return get_tyk_api(TykAssetsApi, api_key, override_base_url)

def get_tyk_policies_api(api_key: str, override_base_url: str | None = None) -> TykPoliciesApi:
    return get_tyk_api(TykPoliciesApi, api_key, override_base_url)

def get_tyk_certificates_api(api_key: str, override_base_url: str | None = None) -> TykCertificatesApi:
    return get_tyk_api(TykCertificatesApi, api_key, override_base_url)

def get_tyk_identity_management_profiles_api(api_key: str, override_base_url: str | None = None) -> TykIdentityManagementProfilesAPI:
    return get_tyk_api(TykIdentityManagementProfilesAPI, api_key, override_base_url)

def get_tyk_keys_api(api_key: str, override_base_url: str | None = None) -> TykKeysApi:
    return get_tyk_api(TykKeysApi, api_key, override_base_url)

def get_tyk_webhooks_api(api_key: str, override_base_url: str | None = None) -> TykWebHooksApi:
    return get_tyk_api(TykWebHooksApi, api_key, override_base_url)

# ----------------------------------------------------------------------
# Admin API accessors
# ----------------------------------------------------------------------

def get_tyk_users_admin_api(override_base_url: str | None = None) -> TykUsersAdminApi:
    return get_tyk_api(TykUsersAdminApi, None, override_base_url)

def get_tyk_organizations_api(override_base_url: str | None = None) -> TykOrganizationsApi:
    return get_tyk_api(TykOrganizationsApi, None, override_base_url)
