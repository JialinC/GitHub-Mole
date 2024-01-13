from typing import List, Dict, Any
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import backend.app.services.github_query.utils.helper as helper

class UserRepositories(PaginatedQuery):
    """
    UserRepositories is a class for querying a user's repositories including details like language statistics,
    fork count, stargazer count, etc. It extends PaginatedQuery to handle potentially large numbers of repositories.
    """
    
    def __init__(self) -> None:
        """
        Initializes a query for a user's repositories with various filtering and ordering options.
        """
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
                                "totalCount",
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
    def user_repositories(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the list of repositories from the raw GraphQL query response data.

        Args:
            raw_data: The raw data returned by the GraphQL query.

        Returns:
            A list of dictionaries, each containing data about a single repository.
        """
        repositories = raw_data.get("user", {}).get("repositories", {}).get("nodes", [])
        return repositories

    @staticmethod
    def cumulated_repository_stats(repo_list: List[Dict[str, Any]], repo_stats: Dict[str, int], lang_stats: Dict[str, int], start: str, end: str, direction: str) -> None:
        """
        Aggregates statistics for repositories created before, after a certain time or in between a time range.

        Args:
            repo_list: List of repositories to be analyzed.
            repo_stats: Dictionary accumulating various statistics like total count, fork count, etc.
            lang_stats: Dictionary accumulating language usage statistics.
            start: String representing the start time for consideration of repositories.
            end: String representing the end time for consideration of repositories.
            direction: Specify whether to aggregates statistics for repositories created before, after a certain time or in between a time range.

        Returns:
            None: Modifies the repo_stats and lang_stats dictionaries in place.
        """
        for repo in repo_list:
            if direction == 'before' and not helper.created_before(repo["createdAt"], start):
                continue
            elif direction == 'after' and not helper.created_after(repo["createdAt"], start):
                continue
            elif direction == 'between' and not helper.in_time_period(repo["createdAt"], start, end):
                continue

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


            
                