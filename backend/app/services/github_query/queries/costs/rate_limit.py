"""The module defines the RateLimit class, which formulates the GraphQL query string
to extract the remaining rate limit of the current user."""

from backend.app.services.github_query.github_graphql.query import QueryNode, Query


class RateLimit(Query):
    """
    RateLimit is a subclass of Query designed to fetch information about the current rate limit status
    of the GitHub API, including the cost of the last query, remaining quota, and reset time.
    """

    def __init__(self) -> None:
        """
        Initializes the RateLimit query with predefined fields to retrieve rate limit information.
        The 'rateLimit' field is a special field in the GitHub GraphQL API that provides rate limit status.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "rateLimit",
                    args={
                        "dryRun": "$dryrun"  # Indicates whether the rate limit should be checked in dry run mode.
                    },
                    fields=[
                        "cost",  # The cost of the last query counted against the rate limit.
                        "limit",  # The maximum number of points the client is permitted to consume in a window of time.
                        "remaining",  # The remaining number of points the client can consume.
                        "resetAt",  # The time at which the current rate limit window resets in UTC epoch seconds.
                        "used",  # The number of points used in the current rate limit window.
                    ],
                )
            ]
        )
