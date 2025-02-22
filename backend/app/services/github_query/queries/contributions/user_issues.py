"""
This module defines the UserIssues class, which extends the PaginatedQuery class to fetch issues associated with a 
specific user from GitHub using GraphQL.

Classes:
    UserIssues: A class to handle the fetching and processing of user issues data from GitHub.

Functions:
    user_issues(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        Extracts issues from the raw data returned by a GraphQL query.
        
    created_before_time(issues: Dict[str, Any], time: str) -> int:
        Counts the number of issues created before a specified time.
"""

from typing import List, Dict, Any
from app.services.github_query.utils.helper import created_before
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    NODE_USER,
    NODE_ISSUES,
    NODE_NODES,
    NODE_PAGE_INFO,
    FIELD_LOGIN,
    FIELD_CREATED_AT,
    FIELD_BODY_TEXT,
    FIELD_TITLE,
    FIELD_ID,
    FIELD_TOTAL_COUNT,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    ARG_LOGIN,
    ARG_FIRST,
)


class UserIssues(PaginatedQuery):
    """
    UserIssues extends PaginatedQuery to fetch issues associated with a specific user.
    It is designed to navigate through potentially large sets of issues data.
    """

    def __init__(self, login: str, pg_size: int = 50) -> None:
        """
        Initializes the UserIssues query with necessary fields and pagination support.

        Args:
            login (str): GitHub username.
            pg_size (int): Number of issues per page (default: 50).
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        FIELD_LOGIN,
                        QueryNodePaginator(
                            NODE_ISSUES,
                            args={ARG_FIRST: pg_size},
                            fields=[
                                FIELD_TOTAL_COUNT,
                                QueryNode(
                                    NODE_NODES,
                                    fields=[
                                        FIELD_CREATED_AT,
                                        FIELD_BODY_TEXT,
                                        FIELD_TITLE,
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
    def user_issues(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts issues from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of issues, each represented as a dictionary.
        """
        return raw_data.get(NODE_USER, {}).get(NODE_ISSUES, {})

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
            if created_before(issue.get(FIELD_CREATED_AT, ""), time):
                counter += 1
            else:
                break
        return counter
