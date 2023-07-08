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

    @staticmethod
    def extract_unique_author(raw_data: dict):
        """
        Extract all unique logins
        Args:
            raw_data: the raw data returned by the query
        Returns:
            set: a set of unique logins
        """
        unique_logins = set()
        nodes = raw_data['repository']['defaultBranchRef']['target']['history']['nodes']
        for node in nodes:
            login = node['author']['user']['login'] if node['author'] and node['author']['user'] else None
            if login:
                unique_logins.add(login)
        return unique_logins

