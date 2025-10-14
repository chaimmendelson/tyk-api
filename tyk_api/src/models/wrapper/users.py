
from enum import Enum


class MainUserTypes(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    BASIC_USER = "basic_user"
    GATEWAY_USER = "gateway_user"