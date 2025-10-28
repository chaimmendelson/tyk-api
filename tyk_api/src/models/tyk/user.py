from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional
from datetime import datetime

from .usergroup import TykUserGroupPermissions


class TykUserAdminPermissions(str, Enum):
    ADMIN = "admin"

class TykUserPermissionsModel(TykUserGroupPermissions):
    IsAdmin: Optional[TykUserAdminPermissions] = None
    ResetPassword: Optional[TykUserAdminPermissions] = None

class TykUserModel(BaseModel):
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[EmailStr] = None
    password: Optional[str] = None
    org_id: Optional[str] = None
    active: Optional[bool] = True
    access_key: Optional[str] = None
    user_permissions: Optional[TykUserPermissionsModel] = TykUserPermissionsModel()
    group_id: Optional[str] = ""
    password_max_days: Optional[int] = None
    password_updated: Optional[datetime] = None
    last_login_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    @property
    def get_access_key(self) -> str:
        
        if not self.access_key:
            raise ValueError("Access key is not set")
        
        return self.access_key

class TykUserCreateModel(BaseModel):
    first_name: str
    last_name: str
    email_address: EmailStr
    password: Optional[str] = Field(
        default=None,
        min_length=8
    )
    org_id: Optional[str] = None
    active: Optional[bool] = True
    user_permissions: Optional[TykUserPermissionsModel] = TykUserPermissionsModel()
    group_id: Optional[str] = ""
    password_max_days: Optional[int] = None

class TykUserUpdateModel(TykUserCreateModel):
    id: str


