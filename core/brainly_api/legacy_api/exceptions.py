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


class QuestionDoesNotExistException(Exception):
    question_id: int

    def __init__(self, question_id: int):
        self.question_id = question_id

        super().__init__(f"Question {question_id} does not exist")
