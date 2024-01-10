from typing import Dict, Any, List
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import backend.app.services.github_query.utils.helper as helper

class UserIssueComments(PaginatedQuery):
    """
    UserIssueComments constructs a paginated GraphQL query specifically for
    retrieving user issue comments. It extends the PaginatedQuery class to handle
    queries that expect a large amount of data that might be delivered in multiple pages.
    """

    def __init__(self) -> None:
        """
        Initializes the UserIssueComments query with specific fields and arguments
        to retrieve user issue comments, including pagination handling. The query is constructed
        to fetch various details about the comments, such as creation time and pagination info.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "issueComments",
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
    def user_issue_comments(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts and returns the issue comments from the raw query data.

        Args:
            raw_data (dict): The raw data returned by the GraphQL query. It's expected
                             to follow the structure: {user: {issueComments: {nodes: [{createdAt: ""}, ...]}}}.
        
        Returns:
            list: A list of dictionaries, each representing an issue comment and its associated data, particularly the creation date.
        """
        issue_comments = raw_data["user"]["issueComments"]["nodes"]
        return issue_comments

    @staticmethod
    def created_before_time(issue_comments: List[Dict[str, Any]], time: str) -> int:
        """
        Counts how many issue comments were created before a specific time.

        Args:
            issue_comments (list): A list of issue comment dictionaries, each containing a "createdAt" field.
            time (str): The cutoff time as a string. All comments created before this time will be counted.

        Returns:
            int: The count of issue comments created before the specified time.
        """
        counter = 0
        for issue_comment in issue_comments:
            if helper.created_before(issue_comment["createdAt"], time):
                counter += 1
            else:
                break
        return counter


