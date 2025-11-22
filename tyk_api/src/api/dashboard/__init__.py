from .apis import TykApisApi
from .assets import TykAssetsApi
from .certificates import TykCertificatesApi
from .keys import TykKeysApi
from .policies import TykPoliciesApi
from .usergroups import TykUserGroupsAPI
from .users import TykUsersApi
from .webhooks import TykWebHooksApi

__all__ = [
    "TykApisApi",
    "TykAssetsApi",
    "TykCertificatesApi",
    "TykKeysApi",
    "TykPoliciesApi",
    "TykUserGroupsAPI",
    "TykUsersApi",
    "TykWebHooksApi",
]