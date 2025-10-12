from pydantic import BaseModel
from typing import Optional, List, Dict


class TykIdentityManagementProfileUseProviderModel(BaseModel):
    DiscoverURL: Optional[str] = None
    Key: Optional[str] = None
    Name: Optional[str] = None
    Scopes: Optional[str] = None
    Secret: Optional[str] = None
    SkipUserInfoRequest: Optional[bool] = False


class TykIdentityManagementProfileProviderConfigModel(BaseModel):
    CallbackBaseURL: Optional[str] = None
    FailureRedirect: Optional[str] = None
    UseProviders: Optional[List[TykIdentityManagementProfileUseProviderModel]] = None


class TykIdentityManagementProfileIdentityHandlerConfigModel(BaseModel):
    DashboardCredential: Optional[str] = None


class TykIdentityManagementProfileProviderConstraintsModel(BaseModel):
    Domain: Optional[str] = None
    Group: Optional[str] = None


class TykIdentityManagementProfileModel(BaseModel):
    ID: str
    Name: Optional[str] = None
    OrgID: Optional[str] = None
    ActionType: str = "GenerateOrLoginUserProfile"
    MatchedPolicyID: Optional[str] = None
    Type: str = "redirect"
    ProviderName: str = "SocialProvider"
    CustomEmailField: Optional[str] = None
    CustomUserIDField: Optional[str] = None
    ProviderConfig: Optional[TykIdentityManagementProfileProviderConfigModel] = None
    IdentityHandlerConfig: Optional[TykIdentityManagementProfileIdentityHandlerConfigModel] = None
    ProviderConstraints: Optional[TykIdentityManagementProfileProviderConstraintsModel] = None
    ReturnURL: Optional[str] = None
    DefaultUserGroupID: Optional[str] = None
    CustomUserGroupField: Optional[str] = None
    UserGroupMapping: Optional[Dict[str, str]] = None
    UserGroupSeparator: Optional[str] = None
    SSOOnlyForRegisteredUsers: Optional[bool] = None
