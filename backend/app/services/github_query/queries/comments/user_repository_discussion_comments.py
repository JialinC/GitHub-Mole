"""
This module defines the UserRepositoryDiscussionComments class, which constructs and handles
paginated GraphQL queries for retrieving user repository discussion comments from GitHub.
It includes methods for extracting and processing the comments data, such as counting comments
created before a specific time.

Classes:
    UserRepositoryDiscussionComments: Constructs and handles the paginated GraphQL query for
    retrieving user repository discussion comments, and provides methods for data extraction
    and processing.

Functions:
    user_repository_discussion_comments(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        Extracts and returns the repository discussion comments from the raw query data.

    created_before_time(repository_discussion_comments: List[Dict[str, Any]], time: str) -> int:
        Counts how many repository discussion comments were created before a specific time.
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
    NODE_REPOSITORY_DISCUSSION_COMMENTS,
    NODE_NODES,
    NODE_PAGE_INFO,
    ARG_LOGIN,
    ARG_FIRST,
)


class UserRepositoryDiscussionComments(PaginatedQuery):
    """
    UserRepositoryDiscussionComments constructs a paginated GraphQL query specifically for
    retrieving user repository discussion comments. It extends the PaginatedQuery class to handle
    queries that expect a large amount of data that might be delivered in multiple pages.
    """

    def __init__(self, login: str, pg_size: int = 50) -> None:
        """
        Initializes the UserRepositoryDiscussionComments query with specific fields and arguments
        to retrieve user repository discussion comments, including pagination handling. The query is constructed
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
                            NODE_REPOSITORY_DISCUSSION_COMMENTS,
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
    def user_repository_discussion_comments(
        raw_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extracts and returns the repository discussion comments from the raw query data.

        Args:
            raw_data (dict): The raw data returned by the GraphQL query. It's expected
            to follow the structure: {user: {repositoryDiscussionComments: {nodes: [{createdAt: ""}, ...]}}}.

        Returns:
            list: A list of dictionaries, each representing a repository discussion comment and its associated data,
            particularly the creation date.
        """
        repository_discussion_comments = raw_data[NODE_USER][
            NODE_REPOSITORY_DISCUSSION_COMMENTS
        ]
        return repository_discussion_comments

    @staticmethod
    def created_before_time(
        repository_discussion_comments: List[Dict[str, Any]], time: str
    ) -> int:
        """
        Counts how many repository discussion comments were created before a specific time.

        Args:
            repository_discussion_comments (list): A list of repository discussion comment dictionaries,
            each containing a "createdAt" field.
            time (str): The cutoff time as a string. All comments created before this time will be counted.

        Returns:
            int: The count of repository discussion comments created before the specified time.
        """
        counter = 0
        for repository_discussion_comment in repository_discussion_comments:
            if created_before(repository_discussion_comment[FIELD_CREATED_AT], time):
                counter += 1
            else:
                break
        return counter
