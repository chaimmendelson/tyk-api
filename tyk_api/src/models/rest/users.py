from pydantic import BaseModel, Field

from ...settings import settings
from ...generators import TykUserGenerator
from ...models import TykUserCreateModel, MainUserTypes, MainUserGroups
from ...repositories import TykUserGroupsRepository


class CreateUserRequest(BaseModel):
    
    org_id: str = Field(
        ...,
        description="The organizatiion Id in which you wish to create the user"
    )
    
    username: str = Field(
        ...,
    )
    
    @property
    async def generate_user(self) -> TykUserCreateModel:

        user = TykUserGenerator.generate_clean_user(
            username=self.username,
            org_id=self.org_id
        )
        
        return user

class CreateBasicUserRequest(CreateUserRequest):
    
    password: str = Field(
        ...,
        pattern=settings.PASSWORD_REGEX
    )
    
    @property
    async def generate_user(self) -> TykUserCreateModel:
        
        user_type = MainUserTypes.BASIC_USER
        
        user = TykUserGenerator.generate_basic_user(
            org_id=self.org_id,
            username=self.username,
            password=self.password,
            group_id=await get_usergroup_id(user_type),
        )
        
        return user

class CreateOrgAdminRequest(CreateUserRequest):
    
    password: str = Field(
        ...,
        pattern=settings.PASSWORD_REGEX
    )
    
    @property
    async def generate_user(self) -> TykUserCreateModel:
        
        user = TykUserGenerator.generate_org_admin_user(
            org_id=self.org_id,
            username=self.username,
            password=self.password,
        )
        
        return user

class CreateSuperAdminRequest(CreateUserRequest):
    
    password: str = Field(
        ...,
        pattern=settings.PASSWORD_REGEX
    )
    
    @property
    async def generate_user(self) -> TykUserCreateModel:
        
        user = TykUserGenerator.generate_super_admin_user(
            username=self.username,
            password=self.password,
        )
        
        return user

class CreateGatewayUserRequest(CreateUserRequest):
    
    @property
    async def generate_user(self) -> TykUserCreateModel:
        
        user_type = MainUserTypes.GATEWAY_USER
        
        user = TykUserGenerator.generate_gateway_user(
            org_id=self.org_id,
            username=self.username,
            group_id=await get_usergroup_id(user_type),
        )
        
        return user

class CreateReadOnlyUserRequest(CreateUserRequest):
    
    password: str = Field(
        ...,
        pattern=settings.PASSWORD_REGEX
    )

    @property
    async def generate_user(self) -> TykUserCreateModel:
        
        user_type = MainUserTypes.READ_ONLY_USER
        
        user = TykUserGenerator.generate_basic_user(
            org_id=self.org_id,
            username=self.username,
            password=self.password,
            group_id=await get_usergroup_id(user_type),
        )
        
        return user
    
class DeleteUserRequest(BaseModel):
    
    org_id: str = Field(
        ...,
        description="The organizatiion Id in which you wish to delete the user"
    )
    
    username: str = Field(
        ...,
    )

class ChangeUserPasswordRequest(BaseModel):

    org_id: str = Field(
        ...,
        description="The organizatiion Id in which you wish to change the user password"
    )

    username: str = Field(
        ...,
    )

    new_password: str = Field(
        ...,
        pattern=settings.PASSWORD_REGEX
    )


async def get_usergroup_id(user_type: MainUserTypes) -> str:
    """Resolve (and ensure) the main usergroup id for a given user type."""
    repo = await TykUserGroupsRepository.instance(admin=True)

    if user_type == MainUserTypes.BASIC_USER:
        group = await repo.ensure_main_usergroup(MainUserGroups.BASIC)
    elif user_type == MainUserTypes.READ_ONLY_USER:
        group = await repo.ensure_main_usergroup(MainUserGroups.READ_ONLY)
    elif user_type == MainUserTypes.GATEWAY_USER:
        group = await repo.ensure_main_usergroup(MainUserGroups.GATEWAY)
    else:
        raise ValueError(f"User type {user_type} does not use a main usergroup")

    return group.id