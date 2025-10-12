from ..base import BaseAPI, TykApi

CERTIFICATES_KEY = "certs"

class TykCertificatesApi(TykApi):
    
    def __init__(
            self,
            api: BaseAPI,
            base_uri: str = "/api/certs",
    ):
        super().__init__(api, base_uri)

    async def get_certificates(self) -> list[str]:
        response = await self.api.client.get(self.base_uri)
        response.raise_for_status()

        object_ids = response.json().get(CERTIFICATES_KEY, []) or []

        return object_ids

    async def delete_certificate(self, certificate_id: str) -> None:

        response = await self.api.client.delete(f"{self.base_uri}/dependencies/{certificate_id}")
        response.raise_for_status()
        
        response = await self.api.client.delete(f"{self.base_uri}/{certificate_id}")
        response.raise_for_status()