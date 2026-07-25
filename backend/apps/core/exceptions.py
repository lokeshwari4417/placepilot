import logging

from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("django")


def custom_exception_handler(exc, context):
    """
    Wraps DRF's default exception handler to return a consistent
    error envelope: { "error": { "code", "message", "details" } }
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        error_payload = {
            "error": {
                "code": response.status_code,
                "message": _extract_message(response.data),
                "details": response.data,
            }
        }
        response.data = error_payload
    else:
        logger.exception("Unhandled exception", exc_info=exc)

    return response


def _extract_message(data):
    if isinstance(data, dict) and "detail" in data:
        return str(data["detail"])
    if isinstance(data, list) and data:
        return str(data[0])
    return "An error occurred."
