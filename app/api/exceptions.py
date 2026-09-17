import logging

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected application errors.

    Internal exception details are logged but are not exposed
    directly to the client.
    """

    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.exception(
        "Unhandled exception | request_id=%s | path=%s",
        request_id,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred.",
            "request_id": request_id,
        },
    )