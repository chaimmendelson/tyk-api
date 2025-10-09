from enum import Enum
from pydantic import BaseModel
from typing import Optional


class PermissionLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    DENY = "deny"


class TykUserGroupPermissions(BaseModel):
    analytics: Optional[PermissionLevel] = None
    api_assets: Optional[PermissionLevel] = None
    apis: Optional[PermissionLevel] = None
    certs: Optional[PermissionLevel] = None
    hooks: Optional[PermissionLevel] = None
    idm: Optional[PermissionLevel] = None
    keys: Optional[PermissionLevel] = None
    log: Optional[PermissionLevel] = None
    oauth: Optional[PermissionLevel] = None
    policies: Optional[PermissionLevel] = None
    portal: Optional[PermissionLevel] = None
    system: Optional[PermissionLevel] = None
    user_groups: Optional[PermissionLevel] = None
    users: Optional[PermissionLevel] = None
    websockets: Optional[PermissionLevel] = None

    class Config:
        use_enum_values = True
