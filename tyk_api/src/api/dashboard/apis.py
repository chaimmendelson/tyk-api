from ..base import BaseAPI, TykDashboardApi

APIS_KEY = "apis"

class TykApisApi(TykDashboardApi):
    
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/apis",
    ):
        super().__init__(api, base_uri)
    
    async def get_apis(self) -> list[str]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()
        
        object_ids = [
            obj.get("api_definition", {}).get("id", "")
            for obj in response.json().get(APIS_KEY, []) or []
        ]
        
        return object_ids
    
    async def get_api(self, api_id: str) -> dict:
        response = await self.api.client.get(f"{self.base_uri}/{api_id}")
        response.raise_for_status()
        
        return response.json()
    
    async def delete_api(self, api_id: str) -> None:
        response = await self.api.client.delete(f"{self.base_uri}/{api_id}")
        response.raise_for_status()