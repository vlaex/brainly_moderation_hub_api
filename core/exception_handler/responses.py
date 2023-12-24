from dataclasses import dataclass


@dataclass
class ErrorResponse:
    error: str
    error_code: str | None
    status: int

    @property
    def data(self):
        data = {
            "error": self.error
        }

        if self.error_code:
            data["error_code"] = self.error_code

        return data
