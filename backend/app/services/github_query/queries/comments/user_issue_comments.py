"""
This module defines the UserIssueComments class, which constructs and handles a paginated
GraphQL query for retrieving user issue comments from GitHub. The query fetches various
details about the comments, such as creation time and pagination info. The module also
provides methods to extract issue comments from raw query data and to count comments
created before a specific time.

Classes:
    UserIssueComments: Handles the construction and execution of the paginated GraphQL query for user issue comments.

Functions:
    user_issue_comments(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        Extracts and returns the issue comments from the raw query data.

    created_before_time(issue_comments: List[Dict[str, Any]], time: str) -> int:
        Counts how many issue comments were created before a specific time.
"""

from typing import Dict, Any, List
from app.services.github_query.utils.helper import created_before
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    FIELD_LOGIN,
    FIELD_TOTAL_COUNT,
    FIELD_CREATED_AT,
    FIELD_BODY_TEXT,
    FIELD_ID,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    NODE_USER,
    NODE_ISSUE_COMMENTS,
    NODE_NODES,
    NODE_PAGE_INFO,
    ARG_LOGIN,
    ARG_FIRST,
)


class UserIssueComments(PaginatedQuery):
    """
    UserIssueComments constructs a paginated GraphQL query specifically for
    retrieving user issue comments. It extends the PaginatedQuery class to handle
    queries that expect a large amount of data that might be delivered in multiple pages.
    """

    def __init__(self, login: str, pg_size: int = 50) -> None:
        """
        Initializes the UserIssueComments query with specific fields and arguments
        to retrieve user issue comments, including pagination handling. The query is constructed
        to fetch various details about the comments, such as creation time and pagination info.

        Args:
            login (str): GitHub username.
            pg_size (int): Number of comments per page (default: 50).
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        FIELD_LOGIN,
                        QueryNodePaginator(
                            NODE_ISSUE_COMMENTS,
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
    def user_issue_comments(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the issue comments from the raw query data.

        Args:
            raw_data (dict): The raw data returned by the GraphQL query. It's expected
                             to follow the structure: {user: {issueComments: {nodes: [{createdAt: ""}, ...]}}}.

        Returns:
            list: A list of dictionaries, each representing an issue comment and its associated data,
            particularly the creation date.
        """
        issue_comments = raw_data[NODE_USER][NODE_ISSUE_COMMENTS]
        return issue_comments

    @staticmethod
    def created_before_time(issue_comments: List[Dict[str, Any]], time: str) -> int:
        """
        Counts how many issue comments were created before a specific time.

        Args:
            issue_comments (list): A list of issue comment dictionaries, each containing a "createdAt" field.
            time (str): The cutoff time as a string. All comments created before this time will be counted.

        Returns:
            int: The count of issue comments created before the specified time.
        """
        counter = 0
        for issue_comment in issue_comments:
            if created_before(issue_comment[FIELD_CREATED_AT], time):
                counter += 1
            else:
                break
        return counter
