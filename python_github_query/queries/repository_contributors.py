from python_github_query.github_graphql.query import QueryNode, Query


class RepositoryContributors(Query):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "repository",
                    args={"owner": "$owner",
                          "name": "$repo_name"},
                    fields=[
                        QueryNode(
                            "defaultBranchRef",
                            fields=[
                                QueryNode(
                                    "target",
                                    fields=[
                                        QueryNode(
                                            "... on Commit",
                                            fields=[
                                                QueryNode(
                                                    "history",
                                                    fields=[
                                                        QueryNode(
                                                            "nodes",
                                                            fields=[
                                                                QueryNode(
                                                                    "author",
                                                                    fields=[
                                                                        QueryNode(
                                                                            "user",
                                                                            fields=[
                                                                                "login"
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

