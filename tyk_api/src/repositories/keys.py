from tyk_api.src.api import TykKeysApi
from .base import TykDashboardRepository

class TykKeysRepository(TykDashboardRepository[TykKeysApi]):

    api_cls = TykKeysApi

    def __init__(self, api: TykKeysApi, org_id: str):

        if not org_id or not org_id.strip():
            raise ValueError("Organization ID cannot be empty.")

        super().__init__(api, org_id)

    async def get_keys(self) -> list[str]:
        return await self.api.get_keys(self.org_id)

    async def delete_key(self, key_id: str) -> None:
        await self.api.delete_key(key_id)

    async def delete_keys(self, key_ids: list[str]) -> None:
        for key_id in key_ids:
            await self.delete_key(key_id)

    async def delete_all_keys(self) -> None:
        keys = await self.get_keys()
        await self.delete_keys(keys)
