from typing import List, Dict
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import backend.app.services.github_query.utils.helper as helper

class UserRepositoryDiscussions(PaginatedQuery):
    def __init__(self) -> None:
        """Initializes a paginated query for GitHub user repository discussions."""
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "repositoryDiscussions",
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
    def user_repository_discussions(raw_data: Dict) -> List[Dict]:
        """
        Extracts repository discussions from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): Raw data returned by the GraphQL query, expected to contain user's repository discussions.

        Returns:
            List[Dict]: A list of dictionaries, each containing data about a single repository discussion.
        """
        repository_discussions = raw_data.get("user", {}).get("repositoryDiscussions", {}).get("nodes", [])
        return repository_discussions

    @staticmethod
    def created_before_time(repository_discussions: List[Dict], time: str) -> int:
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
            if helper.created_before(repository_discussion.get("createdAt", ""), time):
                counter += 1
            else:
                break
        return counter

