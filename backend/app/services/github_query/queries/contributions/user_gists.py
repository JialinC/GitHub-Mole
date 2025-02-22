"""
This module defines the UserGists class, which constructs and processes paginated GraphQL queries for retrieving user 
gists from GitHub.
Classes:
    UserGists: A class that extends PaginatedQuery to handle queries for user gists, including pagination support.
Functions:
    user_gists(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        Processes raw data to extract user gists information.
    created_before_time(gists: Dict[str, Any], time: str) -> int:
        Counts the gists created before a specified time.
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
    NODE_GISTS,
    NODE_NODES,
    NODE_PAGE_INFO,
    FIELD_LOGIN,
    FIELD_CREATED_AT,
    FIELD_DESCRIPTION,
    FIELD_ID,
    FIELD_TOTAL_COUNT,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    ARG_LOGIN,
    ARG_FIRST,
)


class UserGists(PaginatedQuery):
    """
    UserGists constructs a paginated GraphQL query specifically for retrieving user gists.
    It extends the PaginatedQuery class to handle queries that expect a large amount of data
    that might be delivered in multiple pages.
    """

    def __init__(self, login: str, pg_size: int = 50) -> None:
        """
        Initializes the UserGists query with specific fields and arguments
        to retrieve user gists, including pagination handling.

        Args:
            login (str): GitHub username.
            pg_size (int): Number of gists per page (default: 50).
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        FIELD_LOGIN,
                        QueryNodePaginator(
                            NODE_GISTS,
                            args={ARG_FIRST: pg_size},
                            fields=[
                                FIELD_TOTAL_COUNT,
                                QueryNode(
                                    NODE_NODES,
                                    fields=[
                                        FIELD_CREATED_AT,
                                        FIELD_DESCRIPTION,
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
    def user_gists(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the gists from the raw query data.

        Args:
            raw_data (dict): The raw data returned by the GraphQL query.
            Expected structure: {user: {gists: {nodes: [{createdAt: ""}, ...]}}}.

        Returns:
            list: A list of dictionaries, each representing a gist and its associated data.
        """
        gists = raw_data.get(NODE_USER, {}).get(NODE_GISTS, {})
        return gists

    @staticmethod
    def created_before_time(gists: Dict[str, Any], time: str) -> int:
        """Counts the gists created before a specified time.

        Args:
            gists: A list of gist dictionaries returned by the query.
            time: The time string to compare against, in ISO format.

        Returns:
            The count of gists created before the specified time.
        """
        counter = 0
        for gist in gists:
            if created_before(gist.get(FIELD_CREATED_AT, ""), time):
                counter += 1
            else:
                break
        return counter
