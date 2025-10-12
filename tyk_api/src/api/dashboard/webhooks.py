from ..base import BaseAPI, TykDashboardApi

HOOKS_KEY = "hooks"

class TykWebHooksApi(TykDashboardApi):

    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/hooks",
    ):
        super().__init__(api, base_uri)

    async def get_webhooks(self) -> list[str]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()
        
        object_ids = [
            obj.get("id", "")
            for obj in response.json().get(HOOKS_KEY, []) or []
        ]
        
        return object_ids

    async def delete_webhook(self, webhook_id: str) -> None:
        response = await self.api.client.delete(f"{self.base_uri}/{webhook_id}")
        response.raise_for_status()