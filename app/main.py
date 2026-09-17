from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exceptions import global_exception_handler
from app.api.routes.health import router as health_router
from app.api.routes.incidents import router as incident_router
from app.config import get_settings
from app.middleware.request_id import RequestIDMiddleware
from app.observability.logging import (
    configure_logging,
    get_logger,
)


settings = get_settings()

configure_logging(settings.log_level)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Starting AegisOps | version=%s | environment=%s",
        settings.app_version,
        settings.environment,
    )

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


app.add_middleware(
    RequestIDMiddleware,
)


app.add_exception_handler(
    Exception,
    global_exception_handler,
)


app.include_router(health_router)
app.include_router(incident_router)


@app.get("/")
async def root():
    logger.info("Root endpoint requested")

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }