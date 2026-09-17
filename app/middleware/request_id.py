import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request ID to every incoming HTTP request.

    The request ID can be used to trace a request across
    logs, agent execution, database operations, and tools.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        incoming_request_id = request.headers.get(
            REQUEST_ID_HEADER
        )

        request_id = (
            incoming_request_id
            if incoming_request_id
            else str(uuid.uuid4())
        )

        request.state.request_id = request_id

        response = await call_next(request)

        response.headers[REQUEST_ID_HEADER] = request_id

        return response