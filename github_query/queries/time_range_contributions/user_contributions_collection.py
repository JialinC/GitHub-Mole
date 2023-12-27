from collections import Counter
from github_query.github_graphql.query import QueryNode, Query


class UserContributionsCollection(Query):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        QueryNode(
                            "contributionsCollection",
                            args={"from": "$start", "to": "$end"},
                            fields=[
                                "startedAt",
                                "endedAt",
                                "restrictedContributionsCount",
                                "totalCommitContributions",
                                "totalIssueContributions",
                                "totalPullRequestContributions",
                                "totalPullRequestReviewContributions",
                                "totalRepositoryContributions"
                            ]
                        ),
                    ]
                )
            ]
        )

    @staticmethod
    def user_contributions_collection(cumulated_contributions_collection: dict):
        """
        Return the contributors contribution collection
        Args:
            cumulated_contributions_collection: the raw data returned by the query
        Returns:
        """
        raw_data = cumulated_contributions_collection["user"]["contributionsCollection"]
        contribution_collection = Counter({"res_con": raw_data["restrictedContributionsCount"],
                                           "commit": raw_data["totalCommitContributions"],
                                           "issue": raw_data["totalIssueContributions"],
                                           "pr": raw_data["totalPullRequestContributions"],
                                           "pr_review": raw_data["totalPullRequestReviewContributions"],
                                           "repository": raw_data["totalRepositoryContributions"]})
        return contribution_collection
