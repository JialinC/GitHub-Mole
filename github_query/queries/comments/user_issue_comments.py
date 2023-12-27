from github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator
import github_query.util.helper as helper


class UserIssueComments(PaginatedQuery):
    def __init__(self):
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
    def user_issue_comments(raw_data: dict):
        """
        Return the contributors contribution collection
        Args:
            raw_data: the raw data returned by the query
        Returns:
        """
        issue_comments = raw_data["user"]["issueComments"]["nodes"]
        return issue_comments

    @staticmethod
    def created_before_time(issue_comments: list, time: str):
        """
        Return the contributors contribution collection
        Args:
            issue_comments: the raw data returned by the query
            time:
        Returns:
        """
        counter = 0
        for issue_comment in issue_comments:
            if helper.created_before(issue_comment["createdAt"], time):
                counter += 1
            else:
                break
        return counter


