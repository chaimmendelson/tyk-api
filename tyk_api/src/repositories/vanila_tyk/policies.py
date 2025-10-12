from tyk_api.src.api import TykPoliciesApi
from .base import TykDashboardRepository

class TykPoliciesRepository(TykDashboardRepository[TykPoliciesApi]):

    api_cls = TykPoliciesApi
    
    def __init__(self, api: TykPoliciesApi):
        super().__init__(api)
    
    async def get_policies(self) -> list[str]:
        return await self.api.get_policies()
    
    async def delete_policy(self, policy_id: str) -> None:
        await self.api.delete_policy(policy_id)

    async def delete_policies(self, policy_ids: list[str]) -> None:
        for policy_id in policy_ids:
            await self.delete_policy(policy_id)