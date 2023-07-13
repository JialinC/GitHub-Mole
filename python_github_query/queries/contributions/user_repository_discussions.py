from python_github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import python_github_query.util.helper as helper


class UserRepositoryDiscussions(PaginatedQuery):
    def __init__(self):
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
    def user_repository_discussions(raw_data: dict):
        """
        Return the contributors contribution collection
        Args:
            raw_data: the raw data returned by the query
        Returns:
        """
        repository_discussions = raw_data["user"]["repositoryDiscussions"]["nodes"]
        return repository_discussions

    @staticmethod
    def created_before_time(repository_discussions: list, time: str):
        """
        Return the contributors contribution collection
        Args:
            repository_discussions: the raw data returned by the query
            time:
        Returns:
        """
        counter = 0
        for repository_discussion in repository_discussions:
            if helper.created_before(repository_discussion["createdAt"], time):
                counter += 1
            else:
                break
        return counter
