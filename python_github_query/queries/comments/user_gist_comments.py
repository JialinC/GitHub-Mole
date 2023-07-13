from python_github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import python_github_query.util.helper as helper


class UserGistComments(PaginatedQuery):
    def __init__(self):
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
    def user_gist_comments(raw_data: dict):
        """
        Return the contributors contribution collection
        Args:
            raw_data: the raw data returned by the query
        Returns:
        """
        gist_comments = raw_data["user"]["gistComments"]["nodes"]
        return gist_comments

    @staticmethod
    def created_before_time(gist_comments: list, time: str):
        """
        Return the contributors contribution collection
        Args:
            gist_comments: the raw data returned by the query
            time:
        Returns:
        """
        counter = 0
        for gist_comment in gist_comments:
            if helper.created_before(gist_comment["createdAt"], time):
                counter += 1
            else:
                break
        return counter

