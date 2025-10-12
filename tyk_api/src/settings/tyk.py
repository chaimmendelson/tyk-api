from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings

class TykSettings(BaseSettings):
    
    READ_WRITE_GROUP_NAME: str =  Field(
        default="Read-Write User Group",
        description="The name of the Read-Write user group to be created in Tyk.",
    )
    BASIC_USER_GROUP_NAME: str = Field(
        default="Basic User Group",
        description="The name of the Basic user group to be created in Tyk.",
    )
    READ_ONLY_GROUP_NAME: str = Field(
        default="Read-Only User Group",
        description="The name of the Read-Only user group to be created in Tyk.",
    )
    GATEWAY_USER_GROUP_NAME: str = Field(
        default="Gateway User Group",
        description="The name of the Gateway user group to be created in Tyk.",
    )
    DENY_ALL_GROUP_NAME: str = Field(
        default="Deny-All User Group",
        description="The name of the Deny-All user group to be created in Tyk.",
    )
    
    ADMIN_AUTH: str = Field(
        ...,
        description="The Tyk Admin Auth token.",
    )
    
    SUPER_ADMIN_EMAIL: EmailStr = Field(
        ...,
        description="The email address of the Super Admin user to be created in Tyk.",
    )
    SUPER_ADMIN_PASSWORD: str = Field(
        ...,
        description="The password of the Super Admin user to be created in Tyk.",
    )

    DASHBOARD_URL: str = Field(
        ...,
        description="The URL of the Tyk Dashboard.",
    )

    ORG_ADMIN_EMAIL: EmailStr = Field(
        ...,
        description="The email address of the Organization Admin user to be created in Tyk.",
    )
    
    ORG_ADMIN_PASSWORD: str = Field(
        ...,
        description="The password of the Organization Admin user to be created in Tyk.",
    )

    GATEWAY_USER_EMAIL: EmailStr = Field(
        ...,
        description="The email address of the Gateway user to be created in Tyk.",
    )