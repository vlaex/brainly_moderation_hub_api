class BrainlyGraphqlResponse:
    def __init__(self, response: dict):
        self.data = response.get("data")
        self.errors = response.get("errors") or []
