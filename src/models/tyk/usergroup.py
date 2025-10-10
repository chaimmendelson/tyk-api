from enum import Enum
from pydantic import BaseModel
from typing import Optional


class TykPermissionLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    DENY = "deny"


class TykUserGroupPermissions(BaseModel):
    analytics: Optional[TykPermissionLevel] = None
    api_assets: Optional[TykPermissionLevel] = None
    apis: Optional[TykPermissionLevel] = None
    audit_logs: Optional[TykPermissionLevel] = None
    certs: Optional[TykPermissionLevel] = None
    hooks: Optional[TykPermissionLevel] = None
    idm: Optional[TykPermissionLevel] = None
    keys: Optional[TykPermissionLevel] = None
    log: Optional[TykPermissionLevel] = None
    oauth: Optional[TykPermissionLevel] = None
    policies: Optional[TykPermissionLevel] = None
    portal: Optional[TykPermissionLevel] = None
    system: Optional[TykPermissionLevel] = None
    user_groups: Optional[TykPermissionLevel] = None
    users: Optional[TykPermissionLevel] = None
    websockets: Optional[TykPermissionLevel] = None

    class Config:
        use_enum_values = True


class TykUserGroupModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    org_id: Optional[str] = None
    user_permissions: Optional[TykUserGroupPermissions] = TykUserGroupPermissions()
    description: Optional[str] = None
    active: Optional[bool] = True
    password_max_days: Optional[int] = 0