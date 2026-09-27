from ..repositories import TykOrganizationsRepository, TykUsersRepository, TykUserGroupsRepository
from ..models import CreateApplicationRequest, DeleteApplicationRequest, TykOrganizationModel, TykUserModel
from tyk_api.src.models.wrapper.application import Application

class ApplicationService:

    @staticmethod
    async def get_repo() -> TykUserGroupsRepository:
        return await TykUserGroupsRepository.instance(admin=True)
    
    @staticmethod
    async def create_application(app: CreateApplicationRequest) -> Application:
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

    @staticmethod
    async def get_users_by_application(app: DeleteApplicationRequest) -> list[TykUserModel]:
        repo = await TykUsersRepository.instance()

        users = await repo.get_users()

        app_users = [
            user for user in users if str(user.email_address).startswith(app.app_name)
        ]

        return app_users

    @staticmethod
    async def from_name(cls, name: str) -> "Application":
        repo = await TykUserGroupsRepository.instance()

        usergroup = await repo.get_usergroup_by_name(f"{APPLICATION_PREFIX}{name}")

        return cls(usergroup)

    @staticmethod
    async def create(self, model: CreateApplicationRequest) -> None:
        usergroup = TykUserGroupCreateModel(
            name=f"{APPLICATION_PREFIX}{model.name}",
            user_permissions=TykUserGroupPermissions(system=TykPermissionLevel.DENY),
            description=json.dumps({
                "application_password": model.password
            })
        )

        repo = await TykUserGroupsRepository.instance()
        await repo.create_usergroup(usergroup)

    def get_model(self) -> ApplicationModel:
        description = json.loads(self._usergoup.description or "{}")

        return ApplicationModel(
            name=self._usergoup.name.removeprefix(APPLICATION_PREFIX),
            password=description.get("application_password", "")
        )

    async def delete(self) -> None:
        repo = await TykUserGroupsRepository.instance()
        await repo.delete_usergroup(await self._usergoup)