import os
from typing import Any
from http import HTTPStatus
from httpx import Client as HttpClient, HTTPError
from core.markets import Market
from .config import LEGACY_API_HOST
from .responses import LegacyApiResponse
from .exceptions import BrainlyLegacyAPIException, BrainlyLegacyAPIRequestException


class BrainlyLegacyAPI:
    """
    Represents the legacy API (REST API) of Brainly.com
    This API Will be replaced with the GraphQL API in the future.
    """

    _client: HttpClient

    def __init__(
        self,
        market: Market,
        api_protocol: int = 28,
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
            base_url=f"http://{self.market.value}.{LEGACY_API_HOST}/api/{api_protocol}",
            headers={
                "X-B-Token-Long": self.token
            } | self.headers,
            timeout=self.timeout,
            http2=True
        )

    def _request(
        self,
        path: str,
        http_method: str | None = "GET",
        data: Any | None = None
    ) -> LegacyApiResponse:
        """Make a request to the API"""
        try:
            r = self._client.request(
                method=http_method,
                url=path,
                json=data
            )

            if r.status_code == HTTPStatus.BAD_GATEWAY:
                raise ValueError(f"Response status is {r.status_code}")
            if r.status_code == HTTPStatus.FORBIDDEN and "captcha" in r.text:
                raise ValueError("403 Forbidden error")

            data = r.json()
            if not isinstance(data, dict):
                raise ValueError(f"Unknown response data format: {data}")

            if data.get("success") is False:
                raise BrainlyLegacyAPIException(data)

            return LegacyApiResponse(data)
        except (ValueError, HTTPError) as exc:
            raise BrainlyLegacyAPIRequestException(str(exc))

    def get_me(self):
        return self._request("api_users/me")
