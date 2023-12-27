from github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import github_query.util.helper as helper


class UserGists(PaginatedQuery):
    def __init__(self):
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
    def user_gists(raw_data: dict):
        """
        Return the contributors contribution collection
        Args:
            raw_data: the raw data returned by the query
        Returns:
        """
        gists = raw_data["user"]["gists"]["nodes"]
        return gists

    @staticmethod
    def created_before_time(gists: list, time: str):
        """
        Return the contributors contribution collection
        Args:
            gists: the raw data returned by the query
            time:
        Returns:
        """
        counter = 0
        for gist in gists:
            if helper.created_before(gist["createdAt"], time):
                counter += 1
            else:
                break
        return counter
