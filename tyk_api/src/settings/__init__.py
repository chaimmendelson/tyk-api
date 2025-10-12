from pydantic_settings import SettingsConfigDict

from .syntax import Settings as SyntaxSettings
from .tyk import TykSettings

class Settings(TykSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix="TYK_")
    
    syntax: SyntaxSettings = SyntaxSettings()
    

settings = Settings() # type: ignore
