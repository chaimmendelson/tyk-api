from tyk_api.src.api import TykKeysApi
from .base import TykDashboardRepository

class TykKeysRepository(TykDashboardRepository[TykKeysApi]):

    api_cls = TykKeysApi
    
    def __init__(self, api: TykKeysApi):
        super().__init__(api)

    async def get_keys(self, org_id: str) -> list[str]:
        return await self.api.get_keys(org_id)

    async def delete_key(self, key_id: str) -> None:
        await self.api.delete_key(key_id)

    async def delete_keys(self, key_ids: list[str]) -> None:
        for key_id in key_ids:
            await self.delete_key(key_id)
