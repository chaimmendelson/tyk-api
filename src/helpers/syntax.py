import re
from ..settings import settings
from ..errors import TykAPISyntaxError, TykAPIInvalidParameterError

app_regex = settings.syntax.APPLICATION_REGEX_PATTERN
org_regex = settings.syntax.ORGANIZATION_REGEX_PATTERN


def validate_application_name(app_name: str) -> str:
    
    app_name = app_name.lower()
        
    if not re.match(app_regex, app_name):
        raise TykAPIInvalidParameterError(f"Invalid application name: {app_name}")
    
    return app_name

def validate_organization_name(org_name: str) -> str:

    org_name = org_name.lower()

    if not re.match(org_regex, org_name):
        raise TykAPIInvalidParameterError(f"Invalid organization name: {org_name}")

    return org_name
    
def concat_application_organization(app_name: str, org_name: str) -> str:
    
    app_name = validate_application_name(app_name)
    org_name = validate_organization_name(org_name)
    
    return f"{org_name}.{app_name}"

def does_application_exist(existing_apps: list, new_app_name: str) -> bool:
    new_app_name = validate_application_name(new_app_name)
    
    return (
        new_app_name in existing_apps
    )

def does_organization_exist(existing_orgs: list, new_org_name: str, app_name: str) -> bool:
    new_org_name = validate_organization_name(new_org_name)
    
    combined_name = concat_application_organization(app_name, new_org_name)

    return combined_name in existing_orgs

def split_application_organization(combined_name: str) -> tuple[str, str]:
    
    parts = combined_name.split(".")
    
    if len(parts) < 2:
        raise TykAPISyntaxError(f"Invalid combined application and organization name: {combined_name}")
    
    app_name = parts[-1]
    org_name = ".".join(parts[:-1])
    
    validate_application_name(app_name)
    validate_organization_name(org_name)
    
    return org_name, app_name