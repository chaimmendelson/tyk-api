from typing import Generic, TypeVar, Type
from tyk_api.src.api import TykDashboardApi, TykDashboardAdminApi

T = TypeVar("T", bound=TykDashboardApi)
A = TypeVar("A", bound=TykDashboardAdminApi)


class TykRepository:
    """Base class for all repositories."""
    pass


class TykDashboardRepository(TykRepository, Generic[T]):
    """Repository for dashboard (user-level) APIs."""

    api: T
    api_cls: Type[T]  # class-level API type for factory

    def __init__(self, api: T):
        self.api = api


class TykAdminRepository(TykRepository, Generic[A]):
    """Repository for admin APIs."""

    api: A
    api_cls: Type[A]  # class-level API type for factory

    def __init__(self, api: A):
        self.api = api


class TykHybridRepository(TykRepository, Generic[T, A]):
    """Repository for hybrid APIs (dashboard + admin)."""

    dashboard_api: T
    admin_api: A
    dashboard_api_cls: Type[T]  # class-level API type for factory
    admin_api_cls: Type[A]       # class-level API type for factory

    def __init__(self, dashboard_api: T, admin_api: A):
        self.dashboard_api = dashboard_api
        self.admin_api = admin_api
