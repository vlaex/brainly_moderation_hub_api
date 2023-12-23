import os
from http import HTTPStatus
from httpx import Client as HttpClient
from core.markets import Market
from .config import GRAPHQL_SERVER_URL
from .responses import BrainlyGraphqlResponse
from .exceptions import BrainlyGraphqlException


class BrainlyGraphQLAPI:
    """
    Represents the Brainly GraphQL API (https://brainly.com/graphql)
    """

    _client: HttpClient

    def __init__(
        self,
        market: Market,
        token: str | None = None,
        timeout: int = 20,
        headers: dict[str, str] | None = None
    ):
        if token is None or token == "":
            token_in_env = os.environ.get(f"BRAINLY_AUTH_TOKEN_{market.name}")
            assert token_in_env, f"Brainly auth token is required for market '{market.name}'"
            token = token_in_env

        self.token = token
        self.market = market
        self.headers = headers or {}
        self.timeout = timeout

        self._client = HttpClient(
            base_url=f"{GRAPHQL_SERVER_URL}/{self.market.value}",
            headers={
                "X-B-Token-Long": self.token
            } | self.headers,
            timeout=self.timeout,
            http2=True
        )

    def _make_http_request(self, url: str, method: str, body: dict | None = None) -> dict:
        """Make a plain HTTP request to the Brainly GraphQL API"""
        response = self._client.request(method, url, json=body)

        if response.status_code == HTTPStatus.BAD_GATEWAY:
            raise BrainlyGraphqlException(f"Response status is {response.status_code}")
        if response.status_code == HTTPStatus.FORBIDDEN and "captcha" in response.text:
            raise BrainlyGraphqlException("403 Forbidden. Got a captcha in the response")

        return response.json()

    def execute_query(self, query: str, variables: dict = None) -> BrainlyGraphqlResponse:
        """Execute a GraphQL query/mutation"""
        try:
            http_response = self._make_http_request(
                url="/",
                method="POST",
                body={
                    "query": query.strip(),
                    "variables": variables
                }
            )

            response = BrainlyGraphqlResponse(http_response)

            if len(response.errors) > 0:
                raise BrainlyGraphqlException(message="GraphQL errors", response=response)

            return response
        except BrainlyGraphqlException:
            raise
        except Exception as exc:
            raise BrainlyGraphqlException(str(exc)) from exc
