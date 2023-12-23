from pathlib import Path


def use_graphql_query(query_name: str) -> str:
    file_path = Path(__file__).parent.resolve()
    with open(f"{file_path}/graphql_queries/{query_name}.graphql", encoding="utf-8") as f:
        content = f.read()
        return content
