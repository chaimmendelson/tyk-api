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