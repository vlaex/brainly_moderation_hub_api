import pytest
from core.brainly_api.graphql_api import use_graphql_query


def test_use_graphql_query_nonexistent_query():
    query_name = "nonexistent_query"

    with pytest.raises(FileNotFoundError):
        use_graphql_query(query_name)
