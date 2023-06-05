from github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserContributions:
    query = PaginatedQuery(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    "login",
                    QueryNodePaginator(
                        "$contribution_type",
                        fields=[
                            QueryNode(
                                "nodes",
                                fields=["createdAt"]
                            )
                        ]
                    )
                ]
            )
        ]
    )


