from core.brainly_api.legacy_api import BrainlyLegacyAPIException, QuestionDoesNotExistException


def test_brainly_legacy_api_exception():
    response_data = {
        "exception_type": 123,
        "message": "Test Exception",
        "success": False
    }
    exception = BrainlyLegacyAPIException(response_data)

    assert exception.exception_type == response_data["exception_type"]
    assert exception.error_message == response_data["message"]
    assert exception.error_response == response_data


def test_question_does_not_exist_exception(faker):
    question_id = faker.pyint()
    exception = QuestionDoesNotExistException(question_id)

    assert exception.question_id == question_id
