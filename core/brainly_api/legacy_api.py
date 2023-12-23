import os
from typing import Any
from http import HTTPStatus
from httpx import Client as HttpClient, HTTPError
from core.markets import Market
from .config import LEGACY_API_HOST
from .responses import LegacyApiResponse
from .exceptions import BrainlyLegacyAPIException, BrainlyLegacyAPIRequestException, QuestionDoesNotExistException


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
        """Get information about the authenticated user."""
        return self._request("api_users/me")

    def get_user_profile(self, user_id: int):
        """Get the profile of a specific user."""
        return self._request(f"api_user_profiles/get_by_id/{user_id}")

    def get_question(self, question_id: int):
        """
        Get information about a specific question by its ID.

        Raises:
            QuestionDoesNotExistException: If the question does not exist.
        """
        try:
            question = self._request(f"api_tasks/main_view/{question_id}")

            if question.data["task"]["user_id"] == 0:
                raise QuestionDoesNotExistException(question_id)

            return question
        except BrainlyLegacyAPIException as exc:
            if exc.exception_type_eq(40):
                raise QuestionDoesNotExistException(question_id)

            raise

    def get_question_log(self, question_id: int):
        """
        Get the log information for a specific question by its ID.

        Raises:
            QuestionDoesNotExistException: If the question does not exist.
        """
        try:
            return self._request(f"api_task_lines/big/{question_id}")
        except BrainlyLegacyAPIException as exc:
            if exc.exception_type_eq(170):
                raise QuestionDoesNotExistException(question_id)

            raise

    def send_message(self, user_id: int, text: str):
        """Send a message to a specific user."""
        conversation = self._request("api_messages/check", "POST", {
            "user_id": user_id
        })

        conversation_id = conversation.data["conversation_id"]

        return self._request("api_messages/send", "POST", {
            "content": text,
            "conversation_id": conversation_id
        })
