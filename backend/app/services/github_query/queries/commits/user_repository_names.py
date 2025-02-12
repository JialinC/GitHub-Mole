"""The module defines the UserRepositories class, which formulates the GraphQL query string
to extract repositories created by the user based on a given user ID."""

from typing import List, Dict, Any
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    NODE_USER,
    FIELD_ID,
    FIELD_NAME,
    FIELD_TOTAL_COUNT,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    NODE_REPOSITORIES,
    NODE_NODES,
    NODE_PAGE_INFO,
    ARG_LOGIN,
    ARG_FIRST,
    NODE_OWNER,
    FIELD_LOGIN,
)


class UserRepositoryNames(PaginatedQuery):
    """
    UserRepositories is a class for querying a user's repositories including details like language statistics,
    fork count, stargazer count, etc. It extends PaginatedQuery to handle potentially large numbers of repositories.
    """

    def __init__(
        self,
        login: str,
        pg_size: int = 50,
    ) -> None:
        """
        Initializes a query for a user's repositories with various filtering and ordering options.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        FIELD_ID,
                        QueryNodePaginator(
                            NODE_REPOSITORIES,
                            args={ARG_FIRST: pg_size},
                            fields=[
                                FIELD_TOTAL_COUNT,
                                QueryNode(
                                    NODE_NODES,
                                    fields=[
                                        FIELD_NAME,
                                        QueryNode(NODE_OWNER, fields=[FIELD_LOGIN]),
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
    def user_repository_names(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the list of repositories from the raw GraphQL query response data.

        Args:
            raw_data: The raw data returned by the GraphQL query.

        Returns:
            A list of dictionaries, each containing data about a single repository.
        """
        return raw_data.get(NODE_USER, {}).get(NODE_REPOSITORIES, {}), raw_data.get(
            NODE_USER, {}
        ).get(FIELD_ID)
