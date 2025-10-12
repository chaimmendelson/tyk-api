from ..base import BaseAPI, TykApi

POLICIES_KEY = "Data"

class TykPoliciesApi(TykApi):
    
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/portal/policies",
    ):
        super().__init__(api, base_uri)
    
    async def get_policies(self) -> list[str]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()
        
        object_ids = [
            obj.get("_id", "")
            for obj in response.json().get(POLICIES_KEY, []) or []
        ]
        
        return object_ids

    async def delete_policy(self, policy_id: str) -> None:
        response = await self.api.client.delete(f"{self.base_uri}/{policy_id}")
        response.raise_for_status()