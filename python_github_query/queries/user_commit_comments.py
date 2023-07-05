from python_github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserCommitComments(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "commitComments",
                            args={"first": "$pg_size"},
                            fields=[
                                "totalCount",
                                QueryNode(
                                    "nodes",
                                    fields=["body", "createdAt"]
                                ),
                                QueryNode(
                                    "pageInfo",
                                    fields=["endCursor", "hasNextPage"]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
