import logging
import time
import uuid

logger = logging.getLogger("django")


class RequestLoggingMiddleware:
    """Attaches a request ID and logs method/path/status/duration for every request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000
        logger.info(
            "%s %s -> %s (%.1fms) [%s]",
            request.method, request.path, response.status_code, duration_ms, request.request_id,
        )
        response["X-Request-ID"] = request.request_id
        return response
