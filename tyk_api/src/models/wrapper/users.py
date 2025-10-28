from enum import Enum
from .usergroups import MainUserGroups

class MainUserTypes(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    BASIC_USER = "basic_user"
    GATEWAY_USER = "gateway_user"
    READ_ONLY_USER = "read_only_user"

    @property
    def usergroup(self) -> MainUserGroups | None:
        match self:
            case MainUserTypes.SUPER_ADMIN:
                return None
            case MainUserTypes.ORG_ADMIN:
                return None
            case MainUserTypes.BASIC_USER:
                return MainUserGroups.BASIC
            case MainUserTypes.GATEWAY_USER:
                return MainUserGroups.GATEWAY
            case MainUserTypes.READ_ONLY_USER:
                return MainUserGroups.READ_ONLY