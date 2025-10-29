from ..repositories import TykApplicationsRepository, TykOrganizationsRepository
from ..models import CreateApplicationRequest, DeleteApplicationRequest, TykOrganizationModel


class ApplicationService:

    @staticmethod
    async def get_repo() -> TykApplicationsRepository:
        return await TykApplicationsRepository.instance(admin=True)
    
    @staticmethod
    async def create_application(app: CreateApplicationRequest) -> None:
        repo = await ApplicationService.get_repo()
        await repo.create_application_usergroup(app.app_name)
    
    @staticmethod
    async def get_applications() -> list[str]:
        repo = await ApplicationService.get_repo()
        return await repo.get_applications()

    @staticmethod
    async def delete_application(app: DeleteApplicationRequest) -> None:
        repo = await ApplicationService.get_repo()
        await repo.delete_application_usergroup(app.app_name)

    @staticmethod
    async def get_organizations_by_application(app: DeleteApplicationRequest) -> list[TykOrganizationModel]:
        orgs_repo = await TykOrganizationsRepository.instance()
        return await orgs_repo.get_organizations_by_application(app.app_name)