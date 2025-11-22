from fastapi import APIRouter, HTTPException
from ..models import (
    TykUserModel,
    CreateBasicUserRequest,
    DeleteUserRequest,
)
from ..services.users import UsersService
from ..errors import TykNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------------------------------------------------
# Users per Organization
# ---------------------------------------------------------

@router.get("/org/{org_id}", response_model=list[TykUserModel])
async def list_users(org_id: str):
    """List all users inside an organization."""
    try:
        return await UsersService.get_users(org_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_model=TykUserModel, status_code=201)
async def create_basic_user(user: CreateBasicUserRequest):
    """Create a new basic user inside an organization."""
    try:
        return await UsersService.create_basic_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("", status_code=200)
async def delete_user(user: DeleteUserRequest):
    """Delete a user from an organization."""
    try:
        await UsersService.delete_user(user)
        return {"detail": "User deleted"}
    except TykNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
