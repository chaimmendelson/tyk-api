from enum import Enum
from pathlib import Path
import yaml

from tyk_api.src.models import TykUserGroupPermissions, TykPermissionLevel
from tyk_api.src.settings import settings


# ------------------------------------------
# Path to permissions YAML file
# ------------------------------------------
PERMISSIONS_FILE = Path(settings.PERMISSIONS_FILE or "permissions.yaml")


def _load_permissions_file() -> dict:
    if not PERMISSIONS_FILE.exists():
        raise FileNotFoundError(f"Permissions file not found: {PERMISSIONS_FILE}")
    return yaml.safe_load(PERMISSIONS_FILE.read_text())


# ------------------------------------------
# Load permissions data
# ------------------------------------------
_RAW_PERMISSIONS = _load_permissions_file()


def _build_permission(group_name: str) -> TykUserGroupPermissions:
    """Build a TykUserGroupPermissions object from YAML data, defaulting to DENY."""
    defaults = {field: TykPermissionLevel.DENY for field in TykUserGroupPermissions.model_fields.keys()}

    provided_raw = _RAW_PERMISSIONS.get(group_name.lower(), {})
    
    if not isinstance(provided_raw, dict):
        raise ValueError(f"Invalid permissions format for group '{group_name}': {provided_raw}")
    
    if not provided_raw:
        raise ValueError(f"No permissions defined for group '{group_name}'")
    
    provided = {
        key: TykPermissionLevel[value.upper()]
        for key, value in provided_raw.items()
    }

    combined = {**defaults, **provided}
    return TykUserGroupPermissions(**combined)


# ------------------------------------------
# Enum for main user groups
# ------------------------------------------
class MainUserGroups(str, Enum):
    GATEWAY = settings.GATEWAY_USER_GROUP_NAME
    READ_WRITE = settings.READ_WRITE_USER_GROUP_NAME
    BASIC = settings.BASIC_USER_GROUP_NAME
    READ_ONLY = settings.READ_ONLY_USER_GROUP_NAME
    DENY_ALL = settings.DENY_ALL_USER_GROUP_NAME

    @property
    def permissions(self) -> TykUserGroupPermissions:
        """Return the permissions object for this group, defaulting to DENY_ALL."""
        try:
            return _build_permission(self.value)
        except Exception:
            # fallback to deny all if anything goes wrong
            return _build_permission(settings.DENY_ALL_USER_GROUP_NAME)
