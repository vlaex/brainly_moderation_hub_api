from core.brainly_api.graphql_api import BrainlyGraphqlException, BrainlyGraphqlResponse


def test_brainly_graphql_exception():
    errors_in_response = [
        {"message": "Syntax Error: Expected Name, found \"}\".", "extensions": {"code": "GRAPHQL_PARSE_FAILED"}}
    ]

    exc = BrainlyGraphqlException(
        "test error",
        response=BrainlyGraphqlResponse(
            {"errors": errors_in_response}
        )
    )

    assert exc.message == "test error"
    assert exc.response_errors == errors_in_response
