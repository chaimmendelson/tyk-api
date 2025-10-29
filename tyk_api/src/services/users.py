from ..repositories import TykUsersRepository
from ..models import TykUserModel, CreateBasicUserRequest, DeleteUserRequest
from ..helpers import create_email
from loguru import logger

class UsersService:

    @staticmethod
    async def get_repo(org_id: str) -> TykUsersRepository:
        return await TykUsersRepository.instance(org_id=org_id)

    @staticmethod
    async def get_users(org_id: str) -> list[TykUserModel]:
        repo = await UsersService.get_repo(org_id=org_id)
        return await repo.get_users_by_organization(org_id=org_id)
    
    @staticmethod
    async def create_basic_user(user: CreateBasicUserRequest) -> TykUserModel:
        repo = await UsersService.get_repo(org_id=user.org_id)
        
        user_model = await repo.create_user(user=await user.generate_user)

        logger.info(f"Created basic user '{user.username}' in organization '{user.org_id}'")
        
        return user_model
    
    @staticmethod
    async def delete_user(user: DeleteUserRequest) -> None:
        repo = await TykUsersRepository.instance(org_id=user.org_id)

        await repo.delete_user_by_email(email=create_email(user.username), org_id=user.org_id)

        logger.info(f"Deleted user '{user.username}' from organization '{user.org_id}'")