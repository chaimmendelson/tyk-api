from tyk_api.src.api import TykAssetsApi
from .base import TykDashboardRepository

class TykAssetsRepository(TykDashboardRepository[TykAssetsApi]):

    api_cls = TykAssetsApi

    def __init__(self, api: TykAssetsApi):
        super().__init__(api)

    async def get_assets(self) -> list[str]:
        return await self.api.get_assets()
    
    async def delete_asset(self, asset_id: str) -> None:
        await self.api.delete_asset(asset_id)
        
    async def delete_assets(self, asset_ids: list[str]) -> None:
        for asset_id in asset_ids:
            await self.delete_asset(asset_id)