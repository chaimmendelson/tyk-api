from ..base import BaseAPI, TykDashboardApi
from tyk_api.src.models import TykIdentityManagementProfileModel

IDENTITY_MANAGEMENT_PROFILES_KEY = "Data"

class TykIdentityManagementProfilesAPI(TykDashboardApi):
    
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/tib/profiles",
    ):
        super().__init__(api, base_uri)
        
    async def get_identity_management_profiles(self) -> list[TykIdentityManagementProfileModel]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()

        profiles_data = response.json().get(IDENTITY_MANAGEMENT_PROFILES_KEY, []) or []
        
        print(profiles_data)

        return [TykIdentityManagementProfileModel.model_validate(profile) for profile in profiles_data]

    async def get_identity_management_profile(self, profile_id: str) -> TykIdentityManagementProfileModel:
        response = await self.api.client.get(f"{self.base_uri}/{profile_id}")
        response.raise_for_status()
        
        return TykIdentityManagementProfileModel.model_validate(response.json())

    async def create_identity_management_profile(self, profile: TykIdentityManagementProfileModel) -> TykIdentityManagementProfileModel:
        
        body = profile.model_dump(exclude_none=True)

        response = await self.api.client.post(self.base_uri, json=body)
        response.raise_for_status()
        
        new_profile = response.json().get(IDENTITY_MANAGEMENT_PROFILES_KEY, {}) or {}

        return TykIdentityManagementProfileModel.model_validate(new_profile)

    async def update_identity_management_profile(self, profile: TykIdentityManagementProfileModel):
        
        body = profile.model_dump(exclude_none=True)
        
        response = await self.api.client.put(f"{self.base_uri}/{profile.ID}", json=body)
        response.raise_for_status()

        new_profile = response.json().get(IDENTITY_MANAGEMENT_PROFILES_KEY, {}) or {}

        return TykIdentityManagementProfileModel.model_validate(new_profile)

    async def delete_identity_management_profile(self, profile: TykIdentityManagementProfileModel):
        response = await self.api.client.delete(f"{self.base_uri}/{profile.ID}")
        response.raise_for_status()