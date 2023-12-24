from core.brainly_api.graphql_utils import str_to_gql_id, gql_id_to_int


def test_str_to_gql_id():
    assert str_to_gql_id("abc") == "YWJj"
    assert str_to_gql_id("123") == "MTIz"
    assert str_to_gql_id("user:3") == "dXNlcjoz"


def test_gql_id_to_int():
    assert gql_id_to_int("YWJj") == 0
    assert gql_id_to_int("MTIz") == 123
    assert  gql_id_to_int("dXNlcjoxNzgzMjU2Nw==") == "user:17832567"


def test_str_to_gql_id_empty_string():
    assert str_to_gql_id("") == ""
