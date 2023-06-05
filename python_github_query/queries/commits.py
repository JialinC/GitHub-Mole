from github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserCommits:
    query = PaginatedQuery(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    QueryNodePaginator(
                        "contributionsCollection",
                        args={"start": "$start", "end": "$end"},
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
