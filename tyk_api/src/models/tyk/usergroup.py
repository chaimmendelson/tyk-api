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
    id: str
    name: Optional[str] = None
    org_id: Optional[str] = None
    user_permissions: Optional[TykUserGroupPermissions] = TykUserGroupPermissions()
    description: Optional[str] = None
    active: Optional[bool] = True
    password_max_days: Optional[int] = 0

    @property
    def update_model(self) -> "TykUserGroupUpdateModel":
        return TykUserGroupUpdateModel(
            id=self.id,
            name=self.name,
            org_id=self.org_id,
            user_permissions=self.user_permissions,
            description=self.description,
            active=self.active,
            password_max_days=self.password_max_days,
        )
    
class TykUserGroupCreateModel(BaseModel):
    name: str
    org_id: Optional[str] = None
    user_permissions: Optional[TykUserGroupPermissions] = TykUserGroupPermissions()
    description: Optional[str] = None
    active: Optional[bool] = True
    password_max_days: Optional[int] = 0


class TykUserGroupUpdateModel(TykUserGroupCreateModel):
    id: str