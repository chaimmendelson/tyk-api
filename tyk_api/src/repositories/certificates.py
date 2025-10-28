from tyk_api.src.api import TykCertificatesApi
from .base import TykDashboardRepository

class TykCertificatesRepository(TykDashboardRepository[TykCertificatesApi]):

    api_cls = TykCertificatesApi

    def __init__(self, api: TykCertificatesApi, org_id: str):
        super().__init__(api, org_id)

    async def get_certificates(self) -> list[str]:
        return await self.api.get_certificates()

    async def delete_certificate(self, cert_id: str) -> None:
        await self.api.delete_certificate(cert_id)

    async def delete_certificates(self, cert_ids: list[str]) -> None:
        for cert_id in cert_ids:
            await self.delete_certificate(cert_id)

    async def delete_all_certificates(self) -> None:
        certs = await self.get_certificates()
        await self.delete_certificates(certs)