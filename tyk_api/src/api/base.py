from __future__ import annotations
from typing import Any, Optional, Self
from horizon_fastapi_template.utils import BaseAPI
from tyk_api.src.settings import settings


class TykApi:
    """Base for all Tyk API clients — does not handle auth itself."""

    def __init__(self, api: BaseAPI, base_uri: str = ""):
        self.api = api
        self.base_uri = base_uri

    @classmethod
    def instance(
        cls,
        *,
        headers: Optional[dict[str, str]] = None,
        override_base_url: Optional[str] = None,
        **kwargs,
    ) -> Self:
        """
        Create instance with basic configuration (no auth applied by default).
        Subclasses may use `key` or `headers` to add auth.
        """
        base_url = override_base_url or settings.DASHBOARD_URL
        api = BaseAPI(base_url=base_url, headers=headers or {})
        return cls(api)


class TykDashboardApi(TykApi):
    """Standard dashboard API that requires a user key."""

    @classmethod
    def instance(
        cls,
        *,
        key: str,
        headers: Optional[dict[str, str]] = None,
        override_base_url: Optional[str] = None,
        **kwargs,
    ) -> Self:
        """

        :rtype: Self
        """
        headers = headers or {}

        headers["Authorization"] = key
        
        # call the base factory which now accepts key (and will ignore it)
        return super().instance(headers=headers, key=key, override_base_url=override_base_url)


class TykDashboardAdminApi(TykApi):
    """Admin Dashboard API — admin-auth comes from settings and cannot be overridden."""

    @classmethod
    def instance(
        cls,
        *,
        headers: Optional[dict[str, str]] = None,
        override_base_url: Optional[str] = None,
        **kwargs,
    ) -> Self:
        headers = headers or {}

        headers["admin-auth"] = settings.ADMIN_AUTH
        
        # call base factory
        return super().instance(headers=headers, override_base_url=override_base_url)
