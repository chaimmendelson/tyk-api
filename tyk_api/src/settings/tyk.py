from pydantic import Field
from pydantic_settings import BaseSettings

class TykSettings(BaseSettings):
    
    READ_WRITE_USER_GROUP_NAME: str =  Field(
        default="Read-Write User Group",
        description="The name of the Read-Write user group to be created in Tyk.",
    )
    BASIC_USER_GROUP_NAME: str = Field(
        default="Basic User Group",
        description="The name of the Basic user group to be created in Tyk.",
    )
    READ_ONLY_USER_GROUP_NAME: str = Field(
        default="Read-Only User Group",
        description="The name of the Read-Only user group to be created in Tyk.",
    )
    GATEWAY_USER_GROUP_NAME: str = Field(
        default="Gateway User Group",
        description="The name of the Gateway user group to be created in Tyk.",
    )
    DENY_ALL_USER_GROUP_NAME: str = Field(
        default="Deny-All User Group",
        description="The name of the Deny-All user group to be created in Tyk.",
    )
    PERMISSIONS_FILE: str = Field(
        default="permissions.yaml",
        description="Path to the YAML file defining user group permissions.",
    )
    
    ADMIN_AUTH: str = Field(
        ...,
        description="The Tyk Admin Auth token.",
    )
    
    EMAIL_DOMAIN: str = Field(
        ...,
        description="The email domain to be used for creating users in Tyk.",
        pattern=r"^[^@]([a-zA-Z0-9]+\.[a-zA-Z0-9]+)$"
    )

    SUPER_ADMIN_USERNAME: str = Field(
        ...,
        description="The username of the Super Admin user to be created in Tyk.",
        pattern=r""
    )
    
    SUPER_ADMIN_PASSWORD: str = Field(
        ...,
        description="The password of the Super Admin user to be created in Tyk.",
    )

    DASHBOARD_URL: str = Field(
        ...,
        description="The URL of the Tyk Dashboard.",
    )

    ORG_ADMIN_USERNAME: str = Field(
        ...,
        description="The username of the Organization Admin user to be created in Tyk.",
    )
    
    ORG_ADMIN_PASSWORD: str = Field(
        ...,
        description="The password of the Organization Admin user to be created in Tyk.",
    )

    GATEWAY_USER_USERNAME: str = Field(
        ...,
        description="The username of the Gateway user to be created in Tyk.",
    )

    PASSWORD_REGEX: str = Field(
        default=r"^(?:[A-Za-z]*\d[A-Za-z\d]*[A-Za-z]+|[A-Za-z]*[A-Za-z]+[A-Za-z\d]*\d)[A-Za-z\d]*$",
        description="The regex pattern for validating user passwords.",
    )
