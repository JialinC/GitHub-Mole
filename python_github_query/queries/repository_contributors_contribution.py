from python_github_query.github_graphql.query import QueryNode, Query


class RepositoryContributorsContribution(Query):
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
                                                    args={"author": "$id"},
                                                    fields=[
                                                        "totalCount",
                                                        QueryNode(
                                                            "nodes",
                                                            fields=[
                                                                "authoredDate",
                                                                "changedFilesIfAvailable",
                                                                "additions",
                                                                "deletions",
                                                                QueryNode(
                                                                    "parents (first: 2)",
                                                                    fields=[
                                                                        "totalCount"
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
