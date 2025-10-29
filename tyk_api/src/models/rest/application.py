from pydantic import BaseModel, Field
from ...settings import settings

class CreateApplicationRequest(BaseModel):
    app_name: str = Field(
        ...,
        pattern=settings.syntax.APPLICATION_REGEX_PATTERN,
    )

class DeleteApplicationRequest(BaseModel):
    app_name: str = Field(
        ...,
        pattern=settings.syntax.APPLICATION_REGEX_PATTERN,
    )