from fastapi import APIRouter, HTTPException
from ..models import TykUserGroupModel
from ..services.usergroups import UserGroupService
from ..errors import TykNotFoundError, TykMultiOperationError

router = APIRouter(prefix="/usergroups", tags=["User Groups"])


# ---------------------------------------------------------
# Organization User Groups
# ---------------------------------------------------------

@router.get("/org/{org_id}", response_model=list[TykUserGroupModel])
async def list_usergroups(org_id: str):
    """List all user groups under an organization."""
    try:
        return await UserGroupService.list_all_usergroups(org_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/org/{org_id}/{usergroup_id}", status_code=200)
async def delete_usergroup(org_id: str, usergroup_id: str):
    """Delete a specific user group by ID."""
    try:
        await UserGroupService.delete_usergroup_by_id(org_id, usergroup_id)
        return {"detail": "User group deleted"}
    except TykNotFoundError:
        raise HTTPException(status_code=404, detail="User group not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/org/{org_id}", status_code=200)
async def delete_all_usergroups(org_id: str):
    """Delete all user groups under an organization."""
    try:
        await UserGroupService.delete_all_usergroups(org_id)
        return {"detail": "All user groups deleted"}
    except TykMultiOperationError as e:
        raise HTTPException(status_code=500, detail=e.errors)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
