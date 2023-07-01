from python_github_query.github_graphql.query import QueryNode, Query


class UserCommits(Query):
    """
    The raw GraphQL query:
    query ($user: String!, $start: DateTime!, $end: DateTime!) {
        user(login: "$user"){
            contributionsCollection(from:"$start",to:"$end"){
                startedAt
                endedAt
                hasActivityInThePast
                hasAnyContributions
                hasAnyRestrictedContributions
                restrictedContributionsCount
                totalCommitContributions
                totalIssueContributions
                totalPullRequestContributions
                totalPullRequestReviewContributions
                totalRepositoriesWithContributedCommits
                totalRepositoriesWithContributedIssues
                totalRepositoriesWithContributedPullRequestReviews
                totalRepositoriesWithContributedPullRequests
                totalRepositoryContributions
            }
        }
    }
    """
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
