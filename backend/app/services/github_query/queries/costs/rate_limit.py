"""The module defines the RateLimit class, which formulates the GraphQL query string
to extract the remaining rate limit of the current user."""

from ..query import QueryNode, Query
from ..constants import (
    NODE_RATE_LIMIT,
    FIELD_LIMIT,
    FIELD_COST,
    FIELD_REMAINING,
    FIELD_RESET_AT,
    FIELD_USED,
    ARG_DRYRUN,
)


class RateLimit(Query):
    """
    RateLimit is a subclass of Query designed to fetch information about the current rate limit status
    of the GitHub API, including the cost of the last query, remaining quota, and reset time.
    """

    def __init__(self, dryrun: bool) -> None:
        """
        Initializes the RateLimit query with predefined fields to retrieve rate limit information.
        The 'rateLimit' field is a special field in the GitHub GraphQL API that provides rate limit status.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_RATE_LIMIT,
                    args={ARG_DRYRUN: dryrun},
                    fields=[
                        FIELD_COST,
                        FIELD_LIMIT,
                        FIELD_REMAINING,
                        FIELD_RESET_AT,
                        FIELD_USED,
                    ],
                )
            ]
        )
