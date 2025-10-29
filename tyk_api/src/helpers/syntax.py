import re
from ..settings import settings
from ..errors import TykAPIInvalidParameterError

app_org_sep = settings.syntax.APPLICATION_ORGANIZATION_SEPARATOR

app_regex = settings.syntax.APPLICATION_REGEX_PATTERN
org_regex = settings.syntax.ORGANIZATION_REGEX_PATTERN


def create_email(username: str) -> str:
    domain = settings.EMAIL_DOMAIN
    return f"{username}@{domain}"

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
    
    if org_name == app_name:
        return app_name
    
    if org_name.startswith(f"{app_name}{app_org_sep}"):
        return org_name
    
    return f"{app_name}{app_org_sep}{org_name}"

def check_application_name(existing_apps: list, new_app_name: str) -> bool:
    new_app_name = validate_application_name(new_app_name)
    
    return (
        new_app_name in existing_apps or
        any(app.startswith(f"{new_app_name}{app_org_sep}") for app in existing_apps)
    )
    
def check_organization_name(existing_orgs: list, new_org_name: str) -> bool:
    new_org_name = validate_organization_name(new_org_name)
    
    return (
        new_org_name in existing_orgs
    )
    
def split_application_organization(combined_name: str, apps: list[str]) -> tuple[str, str]:
    
    for app in apps:
        
        if combined_name == app:
            return app, ""
        
        if combined_name.startswith(f"{app}{app_org_sep}"):
            org_part = combined_name[len(app) + len(app_org_sep):]
            return app, org_part
        
    raise ValueError(f"Could not split combined name: {combined_name}")