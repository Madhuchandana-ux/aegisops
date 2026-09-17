from fastapi import APIRouter

from app.config import get_settings


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check():
    """
    Basic application health check.
    """

    settings = get_settings()

    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }