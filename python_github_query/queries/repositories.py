from github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserRepositories:
    query = PaginatedQuery(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    QueryNodePaginator(
                        "repositories",
                        page_length=10,
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
                                        args={"first": 100},
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
                                    ),
                                ]
                            )
                        ]
                    ),
                ]
            )
        ]
    )

    def __init__(self, is_fork: bool, owner_affiliations: list):
        self.query.fields[0].fields[0].args.update({
            "isFork": is_fork,
            "ownerAffiliations": owner_affiliations,
            "orderBy": {"field": "CREATED_AT", "direction": "ASC"}
        })
