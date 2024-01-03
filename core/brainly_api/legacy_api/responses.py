from typing import Any
from .entities import LegacyApiUser


class LegacyApiResponse:
    protocol_version: str
    data: Any
    users_data: list[LegacyApiUser]

    def __init__(self, response: dict):
        self.protocol_version = response["protocol"]
        self.data = response["data"]

        users_data = response.get("users_data")
        self.users_data = self._parse_users(users_data) if users_data else []

    @staticmethod
    def _parse_users(users: list[dict]) -> list[LegacyApiUser]:
        return [LegacyApiUser.from_dict(user) for user in users]
