from ..base import BaseAPI, TykDashboardApi

class TykAssetsApi(TykDashboardApi):

    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/assets",
    ):
        super().__init__(api, base_uri)

    async def get_assets(self) -> list[str]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()
        
        object_ids = [
            obj.get("_id", "")
            for obj in response.json() or []
        ]
        
        return object_ids

    async def delete_asset(self, asset_id: str) -> None:
        response = await self.api.client.delete(f"{self.base_uri}/{asset_id}")
        response.raise_for_status()