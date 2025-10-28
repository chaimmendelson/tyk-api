from typing import List
from tyk_api.src.api import TykApisApi
from .base import TykDashboardRepository

class TykApisRepository(TykDashboardRepository[TykApisApi]):

    api_cls = TykApisApi
    
    def __init__(self, api: TykApisApi, org_id: str):
        super().__init__(api, org_id)

    async def get_apis(self) -> List[str]:
        return await self.api.get_apis()
    
    async def get_api(self, api_id: str) -> dict:
        return await self.api.get_api(api_id)

    async def delete_api(self, api_id: str) -> None:
        await self.api.delete_api(api_id)
        
    async def delete_apis(self, api_ids: List[str]) -> None:
        for api_id in api_ids:
            await self.delete_api(api_id)

    async def delete_all_apis(self) -> None:
        api_ids = await self.get_apis()
        await self.delete_apis(api_ids)
            