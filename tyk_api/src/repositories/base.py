from __future__ import annotations
from typing import Generic, TypeVar, Type, Self
from tyk_api.src.api import TykDashboardApi, TykDashboardAdminApi
from tyk_api.src.errors import TykAPIError
from .master_users import TykMasterUsersRepository
from httpx import HTTPStatusError
from ..errors import TykAPIError, TykBadRequestError, TykNotFoundError

master_users_repo = TykMasterUsersRepository.instance()

T = TypeVar("T", bound=TykDashboardApi)
A = TypeVar("A", bound=TykDashboardAdminApi)

async def get_key(org_id: str | None = None, admin: bool = False) -> str:
    
    if admin:
        return await master_users_repo.get_super_admin_key()

    if org_id:
        return await master_users_repo.get_org_admin_key(org_id)

    raise TykAPIError("Either org_id or admin must be specified to get an API key")
    
# ---------------------------------------------------------------------
# Base Repository
# ---------------------------------------------------------------------
class TykRepository:
    """Base class for all repositories."""

    @classmethod
    async def instance(cls, *args, **kwargs) -> Self:
        """Base instance builder — subclasses override as needed."""
        return cls(*args, **kwargs)
    
    def handle_response_error(self, error: HTTPStatusError, resource: str, identifier: str = "") -> Exception:
        
        if not error.response:
            raise TykAPIError("No response for the api request")
        
        text = error.response.text or "No content"
        match error.response.status_code:
            
            case 400:
                raise TykBadRequestError(text)
            case 401:
                raise TykBadRequestError(f"User not authorized to perform this request on {resource}")
            case 404:
                raise TykNotFoundError(resource=resource, identifier=identifier)
            case 500:
                raise TykAPIError(f"Error from upstream: {text}")
            case _:
                raise TykAPIError(f"Unhandeld error from upstream, got {error.response.status_code} - {text}")

# ---------------------------------------------------------------------
# Dashboard Repository
# ---------------------------------------------------------------------
class TykDashboardRepository(TykRepository, Generic[T]):
    """Repository for dashboard-level APIs."""
    
    api_cls: Type[T]

    def __init__(self, api: T, org_id: str):
        self.api = api
        self.org_id = org_id

    @classmethod
    async def instance(
        cls,
        *,
        org_id: str | None = None,
        admin: bool = False,
        override_base_url: str | None = None,
    ) -> Self:
        """Return repository instance with a dashboard API."""

        key = await get_key(org_id=org_id, admin=admin)

        api = cls.api_cls.instance(key=key, override_base_url=override_base_url)
        
        return cls(api, org_id if org_id else "")


# ---------------------------------------------------------------------
# Admin Repository
# ---------------------------------------------------------------------
class TykAdminRepository(TykRepository, Generic[A]):
    """Repository for admin-level APIs."""

    api_cls: Type[A]
    
    def __init__(self, api: A):
        self.api = api

    @classmethod
    async def instance(
        cls,
        *,
        override_base_url: str | None = None,
    ) -> Self:
        """Return repository instance with an admin API."""
        api = cls.api_cls.instance(override_base_url=override_base_url)
        return cls(api)


# ---------------------------------------------------------------------
# Hybrid Repository
# ---------------------------------------------------------------------
class TykHybridRepository(TykRepository, Generic[T, A]):
    """Repository combining dashboard and admin APIs."""

    dashboard_api_cls: Type[T]
    admin_api_cls: Type[A]

    def __init__(self, dashboard_api: T, admin_api: A, org_id: str):
        self.dashboard_api = dashboard_api
        self.admin_api = admin_api
        self.org_id = org_id

    @classmethod
    async def instance(
        cls,
        *,
        org_id: str | None = None,
        admin: bool = False,
        override_base_url: str | None = None,
    ) -> Self:
        """Return repository instance with both dashboard and admin APIs."""

        key = await get_key(org_id=org_id, admin=admin)

        dashboard_api = cls.dashboard_api_cls.instance(key=key, override_base_url=override_base_url)
        admin_api = cls.admin_api_cls.instance(override_base_url=override_base_url)
        
        return cls(dashboard_api, admin_api, org_id if org_id else "")
