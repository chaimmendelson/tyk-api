from ..base import BaseAPI, TykDashboardApi

KEYS_KEY = "keys"

class TykKeysApi(TykDashboardApi):

    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/keys",
    ):
        super().__init__(api, base_uri)
    
    async def get_keys(self, org_id: str) -> list[str]:
        response = await self.api.client.get(f"{self.base_uri}/detailed")
        response.raise_for_status()

        keys = response.json().get(KEYS_KEY, []) or []

        object_ids = [
            obj.get("key_hash", "")
            for obj in keys
            if obj.get("data", {}).get("org_id", "") == org_id
        ]
        
        return object_ids

    async def delete_key(self, key_id: str) -> None:
        response = await self.api.client.delete(f"{self.base_uri}/{key_id}")
        response.raise_for_status()