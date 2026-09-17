from contextlib import asynccontextmanager
from app.api.routes.incidents import router as incident_router

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.config import get_settings
from app.observability.logging import (
    configure_logging,
    get_logger,
)


settings = get_settings()

configure_logging(settings.log_level)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when the FastAPI application starts
    and stops.
    """

    logger.info("Starting AegisOps")
    logger.info("Version: %s", settings.app_version)
    logger.info("Environment: %s", settings.environment)

    yield

    logger.info("Stopping AegisOps")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Production-oriented Agentic AI platform "
        "for autonomous IT incident resolution."
    ),
    lifespan=lifespan,
)


app.include_router(health_router)
app.include_router(incident_router)

@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }