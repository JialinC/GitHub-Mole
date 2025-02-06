"""The module defines the QueryCost class, which formulates the GraphQL query string
to calculate the cost of the given GraphQL query."""

from ..query import QueryNode, Query
from ..constants import (
    NODE_RATE_LIMIT,
    FIELD_COST,
    FIELD_REMAINING,
    FIELD_RESET_AT,
    ARG_DRYRUN,
)


class QueryCost(Query):
    """
    QueryCost is a subclass of Query specifically designed to calculate the cost of a GraphQL query.
    It includes the 'rateLimit' field to determine the cost, remaining quota, and reset time for rate limiting purposes.
    """

    def __init__(self, query: str, dryrun: bool) -> None:
        """
        Initializes a QueryCost object with a test query that represents the actual query for which the cost is to be
        calculated.

        Args:
            query (str): The test query to be wrapped within the QueryCost structure.
        """
        if not query:
            raise ValueError("Test query must not be empty")

        super().__init__(
            fields=[
                query,
                QueryNode(
                    NODE_RATE_LIMIT,
                    args={ARG_DRYRUN: dryrun},
                    fields=[
                        FIELD_COST,
                        FIELD_REMAINING,
                        FIELD_RESET_AT,
                    ],
                ),
            ]
        )
