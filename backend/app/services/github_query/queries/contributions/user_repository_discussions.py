"""The module defines the UserRepositoryDiscussions class, which formulates the GraphQL query string
to extract repository discussions created by the user based on a given user ID."""

from typing import List, Dict, Any
from app.services.github_query.utils.helper import created_before
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)

from ..constants import (
    NODE_USER,
    NODE_REPOSITORY_DISCUSSIONS,
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


class UserRepositoryDiscussions(PaginatedQuery):
    """
    UserRepositoryDiscussions is a class for querying a user's repository discussions.
    It extends PaginatedQuery to handle potentially large numbers of repositories.
    """

    def __init__(self, login: str, pg_size: int = 50) -> None:
        """Initializes a paginated query for GitHub user repository discussions."""
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        FIELD_LOGIN,
                        QueryNodePaginator(
                            NODE_REPOSITORY_DISCUSSIONS,
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
    def user_repository_discussions(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts repository discussions from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): Raw data returned by the GraphQL query, expected to contain user's repository discussions.

        Returns:
            List[Dict]: A list of dictionaries, each containing data about a single repository discussion.
        """
        return raw_data.get(NODE_USER, {}).get(NODE_REPOSITORY_DISCUSSIONS, {})

    @staticmethod
    def created_before_time(repository_discussions: Dict[str, Any], time: str) -> int:
        """
        Counts the number of repository discussions created before a specified time.

        Args:
            repository_discussions (List[Dict]): A list of repository discussions dictionaries.
            time (str): The specific time (ISO format) against which to compare the creation dates of the discussions.

        Returns:
            int: The count of repository discussions created before the specified time.
        """
        counter = 0
        for repository_discussion in repository_discussions:
            if created_before(repository_discussion.get(FIELD_CREATED_AT, ""), time):
                counter += 1
            else:
                break
        return counter
