from typing import Type, TypeVar
from tyk_api.src.api import get_tyk_api

from .base import (
    TykDashboardRepository,
    TykAdminRepository,
    TykHybridRepository,
)

# Import all repository classes
from .apis import TykApisRepository
from .assets import TykAssetsRepository
from .certificates import TykCertificatesRepository
from .keys import TykKeysRepository
from .organizations import TykOrganizationsRepository
from .policies import TykPoliciesRepository
from .usergroups import TykUserGroupsRepository
from .users import TykUsersRepository
from .webhooks import TykWebHooksRepository

__all__ = [
    "TykDashboardRepository",
    "TykAdminRepository",
    "TykHybridRepository",

    "TykUsersRepository",
    "TykUserGroupsRepository",
    "TykPoliciesRepository",
    "TykOrganizationsRepository",
    "TykApisRepository",
    "TykAssetsRepository",
    "TykCertificatesRepository",
    "TykKeysRepository",
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

    "R",
]

# ----------------------------------------------------------------------
# Generic type var
# ----------------------------------------------------------------------
R = TypeVar("R", bound=TykDashboardRepository | TykAdminRepository | TykHybridRepository)

# ----------------------------------------------------------------------
# Smart repository factory
# ----------------------------------------------------------------------
def get_tyk_repository(repo_cls: Type[R], api_key: str | None = None) -> R:
    """
    Builds the correct repository instance (dashboard, admin, or hybrid)
    using the class-level API attributes.
    """

    # Dashboard-only repository
    if issubclass(repo_cls, TykDashboardRepository):
        if not api_key:
            raise ValueError(f"API key required for dashboard repository: {repo_cls.__name__}")
        
        repo_instance = repo_cls.__new__(repo_cls)
        api_instance = get_tyk_api(getattr(repo_instance, "api_cls"), api_key)
        return repo_cls(api_instance)

    # Admin-only repository
    if issubclass(repo_cls, TykAdminRepository):
        repo_instance = repo_cls.__new__(repo_cls)
        api_instance = get_tyk_api(getattr(repo_instance, "api_cls"), None)
        return repo_cls(api_instance)

    # Hybrid repository
    if issubclass(repo_cls, TykHybridRepository):
        if not api_key:
            raise ValueError(f"API key required for hybrid repository: {repo_cls.__name__}")
        
        repo_instance = repo_cls.__new__(repo_cls)

        dash_api = get_tyk_api(getattr(repo_instance, "dashboard_api_cls"), api_key)
        admin_api = get_tyk_api(getattr(repo_instance, "admin_api_cls"), None)
        
        return repo_cls(dash_api, admin_api)

    raise TypeError(f"Unsupported repository type: {repo_cls.__name__}")


# ----------------------------------------------------------------------
# Optional explicit accessors for autocompletion
# ----------------------------------------------------------------------
def get_tyk_users_repository(api_key: str) -> TykUsersRepository:
    return get_tyk_repository(TykUsersRepository, api_key)

def get_tyk_usergroups_repository(api_key: str) -> TykUserGroupsRepository:
    return get_tyk_repository(TykUserGroupsRepository, api_key)

def get_tyk_policies_repository(api_key: str) -> TykPoliciesRepository:
    return get_tyk_repository(TykPoliciesRepository, api_key)

def get_tyk_organizations_repository() -> TykOrganizationsRepository:
    return get_tyk_repository(TykOrganizationsRepository)

def get_tyk_apis_repository(api_key: str) -> TykApisRepository:
    return get_tyk_repository(TykApisRepository, api_key)

def get_tyk_assets_repository(api_key: str) -> TykAssetsRepository:
    return get_tyk_repository(TykAssetsRepository, api_key)

def get_tyk_certificates_repository(api_key: str) -> TykCertificatesRepository:
    return get_tyk_repository(TykCertificatesRepository, api_key)

def get_tyk_keys_repository(api_key: str) -> TykKeysRepository:
    return get_tyk_repository(TykKeysRepository, api_key)

def get_tyk_webhooks_repository(api_key: str) -> TykWebHooksRepository:
    return get_tyk_repository(TykWebHooksRepository, api_key)
