from python_github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import python_github_query.util.helper as helper


class UserCommitComments(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "commitComments",
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
    def user_commit_comments(raw_data: dict):
        """
        Return the contributors contribution collection
        Args:
            raw_data: the raw data returned by the query
        Returns:
        """
        commit_comments = raw_data["user"]["commitComments"]["nodes"]
        return commit_comments

    @staticmethod
    def created_before_time(commit_comments: list, time: str):
        """
        Return the contributors contribution collection
        Args:
            commit_comments: the raw data returned by the query
            time:
        Returns:
        """
        counter = 0
        for commit_comment in commit_comments:
            if helper.created_before(commit_comment["createdAt"], time):
                counter += 1
            else:
                break
        return counter
