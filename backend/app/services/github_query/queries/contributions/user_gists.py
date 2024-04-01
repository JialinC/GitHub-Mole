"""The module defines the UserGists class, which formulates the GraphQL query string
to extract gists created by the user based on a given user ID."""

from typing import List, Dict, Any
from backend.app.services.github_query.utils.helper import created_before
from backend.app.services.github_query.github_graphql.query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)


class UserGists(PaginatedQuery):
    """
    UserGists constructs a paginated GraphQL query specifically for retrieving user user gists.
    It extends the PaginatedQuery class to handle queries that expect a large amount of data that might be delivered in
    multiple pages.
    """

    def __init__(self) -> None:
        """Initializes a query for User Gists as a paginated query.

        This query is used to fetch a list of gists for a specific user,
        including pagination support to handle large numbers of gists.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "gists",
                            args={"first": "$pg_size"},
                            fields=[
                                "totalCount",
                                QueryNode("nodes", fields=["createdAt"]),
                                QueryNode(
                                    "pageInfo", fields=["endCursor", "hasNextPage"]
                                ),
                            ],
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def user_gists(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Processes raw data to extract user gists information.

        Args:
            raw_data: The raw data returned by the query, structured as a dictionary.

        Returns:
            A list of dictionaries, each containing data about a single gist.
        """
        gists = raw_data.get("user", {}).get("gists", {}).get("nodes", [])
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
            if created_before(gist.get("createdAt", ""), time):
                counter += 1
            else:
                break
        return counter
