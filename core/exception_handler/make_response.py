from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from django.utils.translation import gettext_lazy as _
from .responses import ErrorResponse


def make_not_authenticated_response(*args) -> ErrorResponse:
    return ErrorResponse(
        error=_("Authentication token not provided"),
        error_code="not_authed",
        status=status.HTTP_401_UNAUTHORIZED
    )


def make_invalid_token_response(*args) -> ErrorResponse:
    return ErrorResponse(
        error=_("Invalid auth token"),
        error_code="invalid_auth_token",
        status=status.HTTP_401_UNAUTHORIZED
    )


def make_interval_error_response(*args) -> ErrorResponse:
    return ErrorResponse(
        error=_("Internal error"),
        error_code="internal_error",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def make_permission_denied_response(*args) -> ErrorResponse:
    return ErrorResponse(
        error=_("You do not have permission to perform this action"),
        error_code="permission_denied",
        status=status.HTTP_403_FORBIDDEN
    )
