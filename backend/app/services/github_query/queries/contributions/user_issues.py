from typing import Dict, List
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import backend.app.services.github_query.utils.helper as helper

class UserIssues(PaginatedQuery):
    """
    UserIssues extends PaginatedQuery to fetch issues associated with a specific user.
    It is designed to navigate through potentially large sets of issues data.
    """
    
    def __init__(self) -> None:
        """
        Initializes the UserIssues query with necessary fields and pagination support.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "issues",
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
    def user_issues(raw_data: Dict) -> List[Dict]:
        """
        Extracts issues from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of issues, each represented as a dictionary.
        """
        return raw_data.get("user", {}).get("issues", {}).get("nodes", [])

    @staticmethod
    def created_before_time(issues: List[Dict], time: str) -> int:
        """
        Counts the number of issues created before a specified time.

        Args:
            issues (List[Dict]): A list of issues, each represented as a dictionary.
            time (str): The time string to compare each issue's creation time against.

        Returns:
            int: The count of issues created before the specified time.
        """
        counter = 0
        for issue in issues:
            if helper.created_before(issue.get("createdAt", ""), time):
                counter += 1
            else:
                break
        return counter
