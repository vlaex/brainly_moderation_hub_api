from rest_framework.views import exception_handler
from rest_framework.response import Response
import logging
from .handlers import handle_not_authenticated_error
from .responses import ErrorResponse


logger = logging.getLogger("app")


EXCEPTION_HANDLERS = {
    "NotAuthenticated": handle_not_authenticated_error
}


def custom_exception_handler(exc, context):
    try:
        exception_class = exc.__class__.__name__

        res = exception_handler(exc, context)

        error_response: ErrorResponse
        if exception_class in EXCEPTION_HANDLERS:
            error_response = EXCEPTION_HANDLERS[exception_class](exc, context, res)
        else:
            message = str(exc)
            error_response = ErrorResponse(error=message, status=res.status_code, error_code=None)

        return Response(data=error_response.data, status=error_response.status)
    except Exception as e:
        logger.error(str(e))
