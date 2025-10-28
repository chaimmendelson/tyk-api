from pydantic import BaseModel, Field

from ...settings import settings
from ...generators import TykUserGenerator
from ...models import TykUserCreateModel, MainUserTypes
from ...repositories import TykUserGroupsRepository

async def get_usergroup_id(user_type: MainUserTypes) -> str:
    
    repo = await TykUserGroupsRepository.instance(admin=True)
    
    if not user_type.usergroup:
        raise ValueError(f"User of type {user_type.value} doesnt have a usergroup name")
    
    usergroup = await repo.get_usergroup_by_name(user_type.usergroup)
    return usergroup.id


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