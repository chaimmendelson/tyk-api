from fastapi import APIRouter, HTTPException
from ..models import (
    CreateOrganizationRequest,
    DeleteOrganizationRequest,
    TykOrganizationModel,
)
from ..services.organization import OrganizationService
from ..errors import TykAPIError, TykBadRequestError

router = APIRouter(prefix="/organizations", tags=["Organizations"])


# ---------------------------------------------------------
# Get organizations for an application
# ---------------------------------------------------------
@router.get("/{app_name}", response_model=list[TykOrganizationModel])
async def list_organizations(app_name: str):
    """
    Return all organizations under an application.
    """
    repo = await OrganizationService.get_repo()
    try:
        return await repo.get_organizations_by_application(
            app_name
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# Create new organization
# ---------------------------------------------------------
@router.post("/", response_model=TykOrganizationModel, status_code=201)
async def create_organization(payload: CreateOrganizationRequest):
    """
    Create a new organization.
    Also validates that the application exists.
    """
    try:
        return await OrganizationService.create_organization(payload)
    except TykBadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TykAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# Delete organization
# ---------------------------------------------------------
@router.delete("/", status_code=200)
async def delete_organization(payload: DeleteOrganizationRequest):
    """
    Deletes:
    - APIs
    - Assets
    - Certificates
    - Policies
    - Keys
    - Webhooks
    - All users
    - All usergroups
    - And finally the organization itself
    """
    try:
        await OrganizationService.delete_organization(payload)
        return {"detail": "Organization deleted"}
    except TykAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
