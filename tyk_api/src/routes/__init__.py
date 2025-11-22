from .applications import router as applications_router
from .organizations import router as organizations_router
from .users import router as users_router
from .usergroups import router as usergroups_router


def add_routers(app):
    """Add all routers to the FastAPI application."""
    app.include_router(applications_router)
    app.include_router(organizations_router)
    app.include_router(users_router)
    app.include_router(usergroups_router)

__all__ = [
    "add_routers",
]