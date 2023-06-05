from github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserComments:
    query = PaginatedQuery(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    "login",
                    QueryNodePaginator(
                        "$comment_type",
                        fields=[
                            QueryNode(
                                "nodes",
                                fields=["body", "createdAt"]
                            )
                        ]
                    )
                ]
            )
        ]
    )
