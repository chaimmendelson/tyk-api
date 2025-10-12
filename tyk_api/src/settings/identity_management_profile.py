from pydantic import Field
from pydantic_settings import BaseSettings
from loguru import logger

class Settings(BaseSettings):
    model_config = {"env_prefix": "TYK_IDENTITY_MANAGEMENT_PROFILE_"}
    
    DASHBOARD_BASE_URL: str = Field(
        description="Base URL for the Tyk Dashboard"
    )
    
    SCOPES: str = Field(
        default="profile email openid",
        description="Default scopes for identity management profiles"
    )
    
    CUSTOM_EMAIL_FIELD: str = Field(
        default="email",
        description="Custom field to be used for email"
    )

    CUSTOM_USER_ID_FIELD: str = Field(
        default="sub",
        description="Custom field to be used for user ID"
    )

    ADMIN_GROUPS: list[str] = Field(
        default_factory=list,
        description="List of admin groups to assign to admin users"
    )
    
    CLIENT_ID: str = Field(
        description="Client ID for the identity provider"
    )
    
    CLIENT_SECRET: str = Field(
        description="Client Secret for the identity provider"
    )
    
    DISCOVERY_URL: str = Field(
        description="Discovery URL for the identity provider"
    )
    