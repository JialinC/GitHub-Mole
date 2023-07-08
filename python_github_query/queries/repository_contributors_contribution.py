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

    @staticmethod
    def user_cumulated_contribution(raw_data: dict):
        """
        Return the cumulated contribution of the contributor
        Args:
            raw_data: the raw data returned by the query
        Returns:
            list: a list of contributor's total additions, total deletions, and total number of commits.
        """
        nodes = raw_data['repository']['defaultBranchRef']['target']['history']['nodes']
        total_additions = 0
        total_deletions = 0
        total_commits = 0
        for node in nodes:
            if node['parents'] and node['parents']['totalCount'] < 2:
                total_additions += node['additions']
                total_deletions += node['deletions']
                total_commits += 1
            else:
                continue
        return [total_commits, total_additions, total_deletions]
