from core.brainly_api.graphql_api import BrainlyGraphqlResponse


def test_brainly_graphql_success_response():
    html_response = {"data": {"userById": {"id": "dXNlcjox"}}}

    response = BrainlyGraphqlResponse(html_response)

    assert response.data == html_response["data"]
    assert response.errors == []


def test_brainly_graphql_error_response():
    html_response = {
        "errors": [{
            "message": "Variable \"$userId\" of required type \"ID!\" was not provided.",
            "extensions": {
                "code": "BAD_USER_INPUT"
            }
        }]
    }

    response = BrainlyGraphqlResponse(html_response)

    assert response.data is None
    assert response.errors == html_response["errors"]
