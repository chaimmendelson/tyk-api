from pydantic import BaseModel
from typing import Optional


class TykOrganizationModel(BaseModel):
    id: str
    cname: Optional[str] = None
    cname_enabled: Optional[bool] = False
    hybrid_enabled: Optional[bool] = True
    owner_name: Optional[str] = None
    owner_slug: Optional[str] = None

class TykOrganizationCreateModel(BaseModel):
    owner_name: str
    owner_slug: str
    cname: Optional[str] = None
    cname_enabled: Optional[bool] = False
    hybrid_enabled: Optional[bool] = True

class TykOrganizationUpdateModel(TykOrganizationCreateModel):
    id: str
