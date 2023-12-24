from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
import logging
from .make_response import make_not_authenticated_response, make_invalid_token_response, make_interval_error_response, \
    make_permission_denied_response
from .responses import ErrorResponse


logger = logging.getLogger("app")


ERROR_RESPONSES = {
    "NotAuthenticated": make_not_authenticated_response,
    "InvalidToken": make_invalid_token_response,
    "PermissionDenied": make_permission_denied_response
}


def custom_exception_handler(exc, context):
    try:
        exception_class = exc.__class__.__name__

        res = exception_handler(exc, context)

        error_response: ErrorResponse

        if isinstance(exc, APIException):
            if exception_class in ERROR_RESPONSES:
                error_response = ERROR_RESPONSES[exception_class](exc, context, res)
            else:
                error_response = ErrorResponse(
                    error=exc.default_detail,
                    status=res.status_code,
                    error_code=exc.default_code
                )
        else:
            logger.exception(exc)
            error_response = make_interval_error_response()

        return Response(data=error_response.data, status=error_response.status)
    except Exception as e:
        logger.exception(e)
