from tyk_api.src.api import TykWebHooksApi
from .base import TykDashboardRepository

class TykWebHooksRepository(TykDashboardRepository[TykWebHooksApi]):

    api_cls = TykWebHooksApi
    
    def __init__(self, api: TykWebHooksApi):
        super().__init__(api)

    async def get_webhooks(self) -> list[str]:
        return await self.api.get_webhooks()
    
    async def delete_webhook(self, webhook_id: str) -> None:
        await self.api.delete_webhook(webhook_id)
        
    async def delete_webhooks(self, webhook_ids: list[str]) -> None:
        for webhook_id in webhook_ids:
            await self.delete_webhook(webhook_id)