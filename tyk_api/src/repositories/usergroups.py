from httpx import HTTPStatusError
from tyk_api.src.api import TykUserGroupsAPI
from tyk_api.src.generators import TykUserGroupGenerator
from tyk_api.src.models import (
    TykUserGroupModel,
    MainUserGroups,
    TykUserGroupCreateModel,
    TykUserGroupUpdateModel,
)
from tyk_api.src.errors import (
    TykNameConflictError,
    TykNotFoundError,
    TykBadRequestError,
)
from .base import TykDashboardRepository

OBJ_NAME = "User group"


class TykUserGroupsRepository(TykDashboardRepository[TykUserGroupsAPI]):
    """Repository managing Tyk user groups for a given organization."""

    api_cls = TykUserGroupsAPI

    def __init__(self, api: TykUserGroupsAPI, org_id: str):
        super().__init__(api, org_id)

    # ---------------------------
    # Generic CRUD operations
    # ---------------------------

    async def get_usergroups(self) -> list[TykUserGroupModel]:
        """Return all user groups belonging to this organization."""
        usergroups = await self.api.get_usergroups()
        return [ug for ug in usergroups if ug.org_id == self.org_id]

    async def get_usergroup_by_id(self, usergroup_id: str) -> TykUserGroupModel:
        """Fetch a specific user group by its ID."""
        try:
            usergroup = await self.api.get_usergroup(usergroup_id)
        except HTTPStatusError as e:
            if e.response.status_code == 404:
                raise TykNotFoundError(OBJ_NAME, f"id='{usergroup_id}'")
            raise

        if usergroup.org_id != self.org_id:
            raise TykNotFoundError(OBJ_NAME, f"id='{usergroup_id}'")

        return usergroup

    async def get_usergroup_by_name(self, name: str) -> TykUserGroupModel:
        """Fetch a specific user group by its name."""
        for usergroup in await self.get_usergroups():
            if usergroup.name == name:
                return usergroup
        raise TykNotFoundError(OBJ_NAME, f"name='{name}'")

    async def create_usergroup(self, usergroup: TykUserGroupCreateModel) -> TykUserGroupModel:
        """Create a new user group."""
        self._validate_name(usergroup.name)

        if await self._exists_by_name(usergroup.name):
            raise TykNameConflictError(OBJ_NAME.lower(), usergroup.name)

        return await self.api.create_usergroup(usergroup)

    async def update_usergroup(self, usergroup: TykUserGroupUpdateModel) -> None:
        """Update an existing user group."""
        self._validate_name(usergroup.name)
        await self.api.update_usergroup(usergroup)

    async def delete_usergroup(self, usergroup: TykUserGroupModel) -> None:
        """Delete a user group."""
        await self.api.delete_usergroup(usergroup)

    async def delete_all_usergroups(self) -> None:
        """Delete all user groups for this organization."""
        for usergroup in await self.get_usergroups():
            await self.delete_usergroup(usergroup)

    # ---------------------------
    # Main (system) user groups
    # ---------------------------

    async def get_main_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        """Fetch a built-in (main) user group by enum value."""
        return await self.get_usergroup_by_name(usergroup.value)

    async def create_main_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        """Create a built-in (main) user group."""
        ug_model = TykUserGroupGenerator.generate_main_usergroups(usergroup)
        return await self.create_usergroup(ug_model)

    async def update_main_usergroup(self, usergroup: MainUserGroups) -> None:
        """Update an existing built-in (main) user group."""
        existing = await self.get_main_usergroup(usergroup)
        ug_model = TykUserGroupGenerator.generate_main_usergroup_update(usergroup, existing.id)
        await self.update_usergroup(ug_model)

    async def delete_main_usergroup(self, usergroup: MainUserGroups) -> None:
        """Delete a built-in (main) user group."""
        existing = await self.get_main_usergroup(usergroup)
        await self.delete_usergroup(existing)

    async def ensure_main_usergroup(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        """Return an existing main user group, or create it if missing."""
        try:
            return await self.get_main_usergroup(usergroup)
        except TykNotFoundError:
            return await self.create_main_usergroup(usergroup)

    async def ensure_main_usergroup_and_update(self, usergroup: MainUserGroups) -> TykUserGroupModel:
        """Ensure a main user group exists, updating it if necessary."""
        try:
            existing = await self.get_main_usergroup(usergroup)
            await self.update_main_usergroup(usergroup)
            return existing
        except TykNotFoundError:
            return await self.create_main_usergroup(usergroup)

    # ---------------------------
    # Private helpers
    # ---------------------------

    async def _exists_by_name(self, name: str) -> bool:
        """Check if a user group with this name already exists."""
        try:
            await self.get_usergroup_by_name(name)
            return True
        except TykNotFoundError:
            return False

    @staticmethod
    def _validate_name(name: str) -> None:
        """Ensure the name is not empty."""
        if not name or not name.strip():
            raise TykBadRequestError(f"{OBJ_NAME} name cannot be empty.")
