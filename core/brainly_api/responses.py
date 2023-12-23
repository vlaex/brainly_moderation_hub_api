from typing import Any


class LegacyApiResponse:
    protocol_version: str
    data: Any
    users_data: list[dict]

    def __init__(self, response: dict):
        self.protocol_version = response["protocol"]
        self.data = response["data"]
        self.users_data = response.get("users_data") or []


class BrainlyGraphqlResponse:
    def __init__(self, response: dict):
        self.data = response.get("data")
        self.errors = response.get("errors") or []
