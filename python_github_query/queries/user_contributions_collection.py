from python_github_query.github_graphql.query import QueryNode, Query


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
                                "hasActivityInThePast",
                                "hasAnyContributions",
                                "hasAnyRestrictedContributions",
                                "restrictedContributionsCount",
                                "totalCommitContributions",
                                "totalIssueContributions",
                                "totalPullRequestContributions",
                                "totalPullRequestReviewContributions",
                                "totalRepositoriesWithContributedCommits",
                                "totalRepositoriesWithContributedIssues",
                                "totalRepositoriesWithContributedPullRequestReviews",
                                "totalRepositoriesWithContributedPullRequests",
                                "totalRepositoryContributions",
                            ]
                        ),
                    ]
                )
            ]
        )
