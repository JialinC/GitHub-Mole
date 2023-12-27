from github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import github_query.util.helper as helper


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

    @staticmethod
    def user_repositories(raw_data: dict):
        """
        Return the contributors contribution collection
        Args:
            raw_data: the raw data returned by the query
        Returns:
        """
        repositories = raw_data["user"]["repositories"]["nodes"]
        return repositories

    @staticmethod
    def cumulated_repository_stats(repo_list: list, repo_stats: dict, lang_stats: dict, end: str):
        for repo in repo_list:
            if helper.created_before(repo["createdAt"], end):
                if repo["languages"]["totalSize"] == 0:
                    continue
                repo_stats["total_count"] += 1
                repo_stats["fork_count"] += repo["forkCount"]
                repo_stats["stargazer_count"] += repo["stargazerCount"]
                repo_stats["watchers_count"] += repo["watchers"]["totalCount"]
                repo_stats["total_size"] += repo["languages"]["totalSize"]
                language_list_sorted = sorted(repo["languages"]["edges"], key=lambda s: s["size"], reverse=True)
                if language_list_sorted:
                    for language in language_list_sorted:
                        name = language["node"]["name"]
                        size = language["size"]
                        if name not in lang_stats:
                            lang_stats[name] = int(size)
                        else:
                            lang_stats[name] += int(size)

