"""The module defines the UserPullRequests class, which formulates the GraphQL query string
to extract pull requests created by the user based on a given user ID."""

from typing import List, Dict, Any
from backend.app.services.github_query.utils.helper import created_before
from backend.app.services.github_query.github_graphql.query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)


class UserPullRequests(PaginatedQuery):
    """
    UserPullRequests extends PaginatedQuery to fetch pull requests associated with a specific user.
    It navigates through potentially large sets of pull request data with pagination.
    """

    def __init__(self) -> None:
        """
        Initializes the UserPullRequests query with necessary fields and pagination support.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "pullRequests",
                            args={"first": "$pg_size"},
                            fields=[
                                "totalCount",
                                QueryNode("nodes", fields=["createdAt"]),
                                QueryNode(
                                    "pageInfo", fields=["endCursor", "hasNextPage"]
                                ),
                            ],
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def user_pull_requests(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts pull requests from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of pull requests, each represented as a dictionary.
        """
        pull_requests = (
            raw_data.get("user", {}).get("pullRequests", {}).get("nodes", [])
        )
        return pull_requests

    @staticmethod
    def created_before_time(pull_requests: Dict[str, Any], time: str) -> int:
        """
        Counts the number of pull requests created before a specified time.

        Args:
            pull_requests (List[Dict]): A list of pull requests, each represented as a dictionary.
            time (str): The time string to compare each pull request's creation time against.

        Returns:
            int: The count of pull requests created before the specified time.
        """
        counter = 0
        for pull_request in pull_requests:
            if created_before(pull_request.get("createdAt", ""), time):
                counter += 1
            else:
                break
        return counter
