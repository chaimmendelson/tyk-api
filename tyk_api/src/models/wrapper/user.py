from enum import Enum
from .usergroup import MainUserGroups

class MainUsers(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    BASIC_USER = "basic_user"
    GATEWAY_USER = "gateway_user"
    READ_ONLY_USER = "read_only_user"

    @property
    async def usergroup_id(self) -> str | None:
        match self:
            case MainUsers.SUPER_ADMIN:
                return None
            case MainUsers.ORG_ADMIN:
                return None
            case MainUsers.BASIC_USER:
                return MainUserGroups.BASIC
            case MainUsers.GATEWAY_USER:
                return await MainUserGroups.GATEWAY.id
            case MainUsers.READ_ONLY_USER:
                return await MainUserGroups.READ_ONLY.id
