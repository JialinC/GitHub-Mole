from typing import Dict, Any, List
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import backend.app.services.github_query.utils.helper as helper

class UserGistComments(PaginatedQuery):
    """
    UserGistComments constructs a paginated GraphQL query specifically for
    retrieving user gist comments. It extends the PaginatedQuery class to handle
    queries that expect a large amount of data that might be delivered in multiple pages.
    """
    def __init__(self) -> None:
        """
        Initializes the UserGistComments query with specific fields and arguments
        to retrieve user gist comments including pagination handling.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "gistComments",
                            args={"first": "$pg_size"},
                            fields=[
                                "totalCount",
                                QueryNode(
                                    "nodes",
                                    fields=["createdAt"]
                                ),
                                QueryNode(
                                    "pageInfo",
                                    fields=["endCursor", "hasNextPage"]
                                )
                            ]
                        )
                    ]
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
            list: A list of dictionaries, each representing a gist comment and its associated data, particularly the creation date.
        """
        gist_comments = raw_data["user"]["gistComments"]["nodes"]
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
            if helper.created_before(gist_comment["createdAt"], time):
                counter += 1
            else:
                break
        return counter

