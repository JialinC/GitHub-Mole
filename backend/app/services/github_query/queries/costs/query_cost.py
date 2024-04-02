"""The module defines the QueryCost class, which formulates the GraphQL query string
to calculate the cost of the given GraphQL query."""

from backend.app.services.github_query.github_graphql.query import QueryNode, Query


class QueryCost(Query):
    """
    QueryCost is a subclass of Query specifically designed to calculate the cost of a GraphQL query.
    It includes the 'rateLimit' field to determine the cost, remaining quota, and reset time for rate limiting purposes.
    """

    def __init__(self, test: str) -> None:
        """
        Initializes a QueryCost object with a test query that represents the actual query for which the cost is to be
        calculated.

        Args:
            test (str): The test query to be wrapped within the QueryCost structure.
        """
        super().__init__(
            fields=[
                test,
                QueryNode(
                    "rateLimit",
                    args={
                        "dryRun": "$dryrun"  # Indicates whether the rate limit should be checked in dry run mode.
                    },
                    fields=[
                        "cost",  # The cost of the last query counted against the rate limit.
                        "remaining",  # The remaining number of points the client can consume.
                        "resetAt",  # The time at which the current rate limit window resets in UTC epoch seconds.
                    ],
                ),
            ]
        )
