from github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import github_query.util.helper as helper


class UserRepositoryDiscussionComments(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "repositoryDiscussionComments",
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
    def user_repository_discussion_comments(raw_data: dict):
        """
        Return the contributors contribution collection
        Args:
            raw_data: the raw data returned by the query
        Returns:
        """
        repository_discussion_comments = raw_data["user"]["repositoryDiscussionComments"]["nodes"]
        return repository_discussion_comments

    @staticmethod
    def created_before_time(repository_discussion_comments: list, time: str):
        """
        Return the contributors contribution collection
        Args:
            repository_discussion_comments: the raw data returned by the query
            time:
        Returns:
        """
        counter = 0
        for repository_discussion_comment in repository_discussion_comments:
            if helper.created_before(repository_discussion_comment["createdAt"], time):
                counter += 1
            else:
                break
        return counter
