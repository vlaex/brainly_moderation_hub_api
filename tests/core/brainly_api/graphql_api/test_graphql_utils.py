import pytest
from core.brainly_api.graphql_api import str_to_gql_id, gql_id_to_int


def test_str_to_gql_id():
    assert str_to_gql_id("abc") == "YWJj"
    assert str_to_gql_id("123") == "MTIz"
    assert str_to_gql_id("user:3") == "dXNlcjoz"


def test_str_to_gql_id_empty_string():
    assert str_to_gql_id("") == ""


def test_gql_id_to_int():
    assert gql_id_to_int("dGFzazoxMDA5MDA=") == 100900
    assert gql_id_to_int("dXNlcjoxNzgzMjU2Nw==") == 17832567


def test_gql_id_to_int_invalid_id():
    with pytest.raises(ValueError):
        gql_id_to_int("YWJj")
