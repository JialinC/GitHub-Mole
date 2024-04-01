"""The module defines the UserIssues class, which formulates the GraphQL query string
to extract issues created by the user based on a given user ID."""

from typing import List, Dict, Any
from backend.app.services.github_query.utils.helper import created_before
from backend.app.services.github_query.github_graphql.query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)


class UserIssues(PaginatedQuery):
    """
    UserIssues extends PaginatedQuery to fetch issues associated with a specific user.
    It is designed to navigate through potentially large sets of issues data.
    """

    def __init__(self) -> None:
        """
        Initializes the UserIssues query with necessary fields and pagination support.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "issues",
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
    def user_issues(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts issues from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of issues, each represented as a dictionary.
        """
        return raw_data.get("user", {}).get("issues", {}).get("nodes", [])

    @staticmethod
    def created_before_time(issues: Dict[str, Any], time: str) -> int:
        """
        Counts the number of issues created before a specified time.

        Args:
            issues (List[Dict]): A list of issues, each represented as a dictionary.
            time (str): The time string to compare each issue's creation time against.

        Returns:
            int: The count of issues created before the specified time.
        """
        counter = 0
        for issue in issues:
            if created_before(issue.get("createdAt", ""), time):
                counter += 1
            else:
                break
        return counter
