import base64


def str_to_gql_id(str_: str) -> str:
    """Encode string to a GraphQL Base64 id"""
    encoded = base64.b64encode(bytes(str_, "utf-8"))

    return encoded.decode("utf-8")


def gql_id_to_int(id_: str) -> int:
    """Decode a GraphQL Base64 id to int"""
    decoded = base64.b64decode(id_)

    decoded_id = decoded.decode("utf-8").split(":").pop()

    return int(decoded_id)
