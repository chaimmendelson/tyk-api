from fastapi import APIRouter, HTTPException
from ..models import (
    CreateApplicationRequest,
    DeleteApplicationRequest,
    TykOrganizationModel,
)
from ..services.applications import ApplicationService

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/", response_model=list[str])
async def list_applications():
    """Return all application names."""
    return await ApplicationService.get_applications()


@router.post("/", status_code=201)
async def create_application(payload: CreateApplicationRequest):
    """Create a new application."""
    try:
        await ApplicationService.create_application(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Application created"}


@router.delete("/", status_code=200)
async def delete_application(payload: DeleteApplicationRequest):
    """Delete an application."""
    try:
        await ApplicationService.delete_application(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Application deleted"}


@router.post("/organizations", response_model=list[TykOrganizationModel])
async def get_organizations_by_application(payload: DeleteApplicationRequest):
    """
    Return a list of organizations belonging to an application.
    Uses DeleteApplicationRequest since it only includes 'app_name'.
    """
    try:
        return await ApplicationService.get_organizations_by_application(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
