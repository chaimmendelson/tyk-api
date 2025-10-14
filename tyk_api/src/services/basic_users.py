from ..repositories import master_users_repo, get_tyk_users_repository, TykUsersRepository, TykMasterUsersRepository
from ..models import TykUserModel, MainUserTypes, MainUserGroups, TykOrganizationModel
from .admin_usergroups import AdminUserGroupService
from ..generators import TykUserGenerator
from ..settings import settings

def get_usergroup(user_type: MainUserTypes) -> MainUserGroups | None:
    match user_type:
        case MainUserTypes.SUPER_ADMIN:
            return None
        case MainUserTypes.ORG_ADMIN:
            return None
        case MainUserTypes.BASIC_USER:
            return MainUserGroups.BASIC
        case MainUserTypes.GATEWAY_USER:
            return MainUserGroups.GATEWAY
        case _:
            return None

class BasicUsersService:

    def __init__(self):
        self.repo: TykUsersRepository | None = None
        self.master_users_repo: TykMasterUsersRepository = master_users_repo
        
    async def _initialize_repo(self) -> None:
        if not self.repo:
            self.repo = await get_tyk_users_repository()

    async def _get_admin_usergroup_service(self) -> AdminUserGroupService:
        admin_usergroup_service = AdminUserGroupService()
        await admin_usergroup_service._initialize_repo()
        return admin_usergroup_service

    async def create_user(self, user_type: MainUserTypes, user: TykUserModel) -> TykUserModel:
        await self._initialize_repo()

        if not self.repo:
            raise ValueError("Users repository not initialized.")

        
        usergroup_api = await self._get_admin_usergroup_service()
        usergroup = get_usergroup(user_type)
        usergroup_id = None
        
        if usergroup is not None:
            usergroup_model = await usergroup_api.get_usergroup(usergroup)
            if usergroup_model is None or usergroup_model.id is None:
                raise ValueError(f"User group '{usergroup}' not found.")
            usergroup_id = usergroup_model.id
        
        user.group_id = usergroup_id

        user = TykUserGenerator.convert_existing_user(user_type, user)

        user = await self.repo.create_user(user)
        
        return user
    
    async def create_main_org_admin_user(self, org: TykOrganizationModel) -> TykUserModel:

        if org.id is None:
            raise ValueError("Organization ID is required to create an org admin user.")
        
        user = await master_users_repo.bootstrap_org_admin(org.id)
        
        return user
    
    async def create_main_gateway_user(self, org: TykOrganizationModel) -> TykUserModel:
        
        if org.id is None:
            raise ValueError("Organization ID is required to create a gateway user.")
        
        user = await self.create_user(
            user_type=MainUserTypes.GATEWAY_USER,
            user=TykUserGenerator.generate_clean_user(
                org_id=org.id,
                username=settings.GATEWAY_USER_USERNAME
            )
        )

        return user