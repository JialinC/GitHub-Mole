"""
This module defines the RateLimit class, a specialized query for fetching rate limit information
from the GitHub API. It provides details about the cost of the last query, the remaining quota,
and the reset time for the rate limit.

Classes:
    RateLimit: A subclass of Query that retrieves rate limit information from the GitHub API.
"""

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

        Args:
            dryrun (bool): A flag indicating whether the query is for rate limit checking only.
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
