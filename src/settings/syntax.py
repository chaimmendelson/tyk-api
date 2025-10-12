from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APPLICATION_ORGANIZATION_SEPARATOR: str = Field(
        default="-",
        description="Separator used between application name and organization name"
    )
    
    APPLICATION_REGEX_PATTERN: str = Field(
        default=r"^[a-zA-Z0-9-]+$",
        description="Regex pattern for validating application names"
    )
    
    ORGANIZATION_REGEX_PATTERN: str = Field(
        default=r"^[a-zA-Z0-9-]+$",
        description="Regex pattern for validating organization names"
    )