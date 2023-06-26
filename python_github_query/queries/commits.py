from python_github_query.github_graphql.query import QueryNode, Query


class UserCommits:
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
    query = Query(
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










#
# {"user" : "JialinC",
# "start" : "2022-02-07T18:11:20Z",
# "end" : "2021-02-07T18:11:20Z"}
#
# "2018-04-20T04:37:16Z"