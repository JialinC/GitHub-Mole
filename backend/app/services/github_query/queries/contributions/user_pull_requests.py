"""The module defines the UserPullRequests class, which formulates the GraphQL query string
to extract pull requests created by the user based on a given user ID."""

from typing import List, Dict, Any
from backend.app.services.github_query.utils.helper import created_before
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    NODE_USER,
    NODE_PULL_REQUESTS,
    NODE_NODES,
    NODE_PAGE_INFO,
    FIELD_LOGIN,
    FIELD_CREATED_AT,
    FIELD_BODY_TEXT,
    FIELD_ID,
    FIELD_TOTAL_COUNT,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    ARG_LOGIN,
    ARG_FIRST,
)


class UserPullRequests(PaginatedQuery):
    """
    UserPullRequests extends PaginatedQuery to fetch pull requests associated with a specific user.
    It navigates through potentially large sets of pull request data with pagination.
    """

    def __init__(self, login: str, pg_size: int = 10) -> None:
        """
        Initializes the UserPullRequests query with necessary fields and pagination support.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        FIELD_LOGIN,
                        QueryNodePaginator(
                            NODE_PULL_REQUESTS,
                            args={ARG_FIRST: pg_size},
                            fields=[
                                FIELD_TOTAL_COUNT,
                                QueryNode(
                                    NODE_NODES,
                                    fields=[
                                        FIELD_CREATED_AT,
                                        FIELD_BODY_TEXT,
                                        FIELD_ID,
                                    ],
                                ),
                                QueryNode(
                                    NODE_PAGE_INFO,
                                    fields=[FIELD_END_CURSOR, FIELD_HAS_NEXT_PAGE],
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
        return (
            raw_data.get(NODE_USER, {}).get(NODE_PULL_REQUESTS, {}).get(NODE_NODES, [])
        )

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
            if created_before(pull_request.get(FIELD_CREATED_AT, ""), time):
                counter += 1
            else:
                break
        return counter
