"""Name/slug helpers used for organizations and applications."""

import re


def _slugify(value: str) -> str:
    """Lowercase, trim, and replace whitespace with hyphens; disallow empty results."""
    slug = re.sub(r"\s+", "-", value.strip().lower())
    if not slug:
        raise ValueError("Name cannot be empty after normalization")
    return slug


def validate_application_name(name: str) -> str:
    """Normalize an application name for use as an owner_slug."""
    return _slugify(name)


def validate_organization_name(name: str) -> str:
    """Normalize an organization name component."""
    return _slugify(name)


def validate_new_application_name(name: str, existing_names: list) -> str:
    """Normalize a new application name, ensuring it doesn't contain an organization prefix."""
    slug = validate_application_name(name)
    
    for existing in existing_names:
        if slug.startswith(existing):
            raise ValueError(f"Application name '{name}' cannot start with an existing organization prefix '{existing}'.")
        if existing.startswith(slug):
            raise ValueError(f"Application name '{name}' cannot be a prefix of an existing organization name '{existing}'.")
        
    return slug

def parse_application_organization(organization: str, existing_applications: list) -> tuple[str, str]:
    """Parse an organization string into application and organization components."""
    for app in existing_applications:
        if organization.startswith(app):
            org_part = organization[len(app):].lstrip("-")
            return app, org_part
    raise ValueError(f"Organization '{organization}' does not start with any known application prefix.")

def concat_application_organization(application: str, organization: str) -> str:
    """Build owner_name: app_org unless org already starts with app, then use org."""
    app = validate_application_name(application)
    org = validate_organization_name(organization)

    if org.startswith(app):
        return org

    return f"{app}-{org}"
