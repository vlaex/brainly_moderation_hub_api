from .responses import BrainlyGraphqlResponse


class BrainlyLegacyAPIException(Exception):
    error_response: dict
    exception_type: int
    error_message: str

    def __init__(self, response: dict):
        self.error_response = response
        self.exception_type = response["exception_type"] or 0
        self.error_message = response.get("message") or ""

        super().__init__(f"{self.error_message}: {str(self.error_response)}")

    def exception_type_eq(self, exception_type: int) -> bool:
        """Check whether the exception type equals another one"""
        return self.exception_type == exception_type


class BrainlyLegacyAPIRequestException(Exception):
    def __init__(self, message: str):
        super().__init__(f"Request to the Brainly legacy API failed: {message}")


class BrainlyGraphqlException(Exception):
    def __init__(self, message, response: BrainlyGraphqlResponse | None = None):
        self.message = message
        self.response_errors = response.errors if response else []

        super().__init__(
            self.message if len(self.response_errors) == 0 else f"{self.message}: {self.response_errors}"
        )
