from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    APPLICATION_USERGROUP_PREFIX: str = Field(
        default="application_usergroup_",
        description="Prefix for application user group names"
    )