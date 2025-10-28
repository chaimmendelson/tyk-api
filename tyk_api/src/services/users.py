from ..repositories import TykUsersRepository
from ..models import TykUserModel, TykOrganizationModel, CreateUserRequest
from ..settings import settings
from loguru import logger


class UsersService:

    @staticmethod
    def build_email(username: str) -> str:
        email = f"{username}@{settings.EMAIL_DOMAIN}"
        logger.debug(f"Built email for username '{username}': {email}")
        return email

    @staticmethod
    async def get_gateway_user(org: TykOrganizationModel) -> TykUserModel | None:
        logger.info(f"Fetching gateway user for organization '{org.id}'")

        repo = await TykUsersRepository.instance(org_id=org.id)
        email = UsersService.build_email(settings.GATEWAY_USER_USERNAME)

        logger.debug(f"Looking for user with email '{email}' in org '{org.id}'")
        users = await repo.get_users_by_email(email=email)

        if users:
            logger.info(f"Gateway user '{users[0].first_name}' found in org '{org.id}'")
            return users[0]

        logger.warning(f"No gateway user found for org '{org.id}'")
        return None

    @staticmethod
    async def ensure_gateway_user(org: TykOrganizationModel) -> TykUserModel:
        logger.info(f"Ensuring gateway user exists for organization '{org.id}'")

        repo = await TykUsersRepository.instance(org_id=org.id)

        # Check if user already exists
        user = await UsersService.get_gateway_user(org)
        if user:
            logger.debug(f"Gateway user already exists for org '{org.id}' ({user.first_name})")
            return user

        # Create new gateway user
        logger.debug(f"Gateway user not found, creating one for org '{org.id}'")
        gateway_user_request = await CreateUserRequest(
            org_id=org.id,
            username=settings.GATEWAY_USER_USERNAME,
        ).generate_user

        created_user = await repo.create_user(gateway_user_request)
        logger.info(f"Gateway user '{created_user.first_name}' created successfully for org '{org.id}'")

        return created_user
