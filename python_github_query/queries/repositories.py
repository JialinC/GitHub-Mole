from python_github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserRepositories(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        QueryNodePaginator(
                            "repositories",
                            args={"first": "$pg_size",
                                  "isFork": "$is_fork",
                                  "ownerAffiliations": "$ownership",
                                  "orderBy": "$order_by"},
                            fields=[
                                QueryNode(
                                    "nodes",
                                    fields=[
                                        "name",
                                        "isEmpty",
                                        "createdAt",
                                        "updatedAt",
                                        "forkCount",
                                        "stargazerCount",
                                        QueryNode("watchers", fields=["totalCount"]),
                                        QueryNode("primaryLanguage", fields=["name"]),
                                        QueryNode(
                                            "languages",
                                            args={"first": 100,
                                                  "orderBy": {"field": "SIZE",
                                                              "direction": "DESC"}},
                                            fields=[
                                                "totalSize",
                                                "totalCount",
                                                QueryNode(
                                                    "edges",
                                                    fields=[
                                                        "size",
                                                        QueryNode("node", fields=["name"])
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                QueryNode(
                                    "pageInfo",
                                    fields=["endCursor", "hasNextPage"]
                                )
                            ]
                        ),
                    ]
                )
            ]
        )

