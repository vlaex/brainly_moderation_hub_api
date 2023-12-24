from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from django.utils.translation import gettext_lazy as _
from .responses import ErrorResponse


def handle_not_authenticated_error(*args) -> ErrorResponse:
    return ErrorResponse(
        error=_("Authentication token not provided"),
        error_code="not_authed",
        status=status.HTTP_401_UNAUTHORIZED
    )
