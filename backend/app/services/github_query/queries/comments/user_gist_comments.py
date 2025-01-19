"""The module defines the UserGistComments class, which formulates the GraphQL query string
to extract gist comments created by the user based on a given user ID."""

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
    NODE_GIST_COMMENTS,
    NODE_NODES,
    NODE_PAGE_INFO,
    ARG_LOGIN,
    ARG_FIRST,
)


class UserGistComments(PaginatedQuery):
    """
    UserGistComments constructs a paginated GraphQL query specifically for
    retrieving user gist comments. It extends the PaginatedQuery class to handle
    queries that expect a large amount of data that might be delivered in multiple pages.
    """

    def __init__(self, login: str, pg_size: int = 10) -> None:
        """
        Initializes the UserGistComments query with specific fields and arguments
        to retrieve user gist comments including pagination handling.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        FIELD_LOGIN,
                        QueryNodePaginator(
                            NODE_GIST_COMMENTS,
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
    def user_gist_comments(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the gist comments from the raw query data.

        Args:
            raw_data (dict): The raw data returned by the GraphQL query, expected
                             to follow the structure: {user: {gistComments: {nodes: [{createdAt: ""}, ...]}}}.

        Returns:
            list: A list of dictionaries, each representing a gist comment and its associated data,
            particularly the creation date.
        """
        gist_comments = raw_data[NODE_USER][NODE_GIST_COMMENTS]
        return gist_comments

    @staticmethod
    def created_before_time(gist_comments: List[Dict[str, Any]], time: str) -> int:
        """
        Counts how many gist comments were created before a specific time.

        Args:
            gist_comments (list): A list of gist comment dictionaries, each containing a "createdAt" field.
            time (str): The cutoff time as a string. All comments created before this time will be counted.

        Returns:
            int: The count of gist comments created before the specified time.
        """
        counter = 0
        for gist_comment in gist_comments:
            if created_before(gist_comment[FIELD_CREATED_AT], time):
                counter += 1
            else:
                break
        return counter
