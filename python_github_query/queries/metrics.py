from python_github_query.github_graphql.query import QueryNode, Query


class UserMetrics:
    query = Query(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    "login",
                    "name",
                    "email",
                    "createdAt",
                    "bio",
                    "company",
                    "isBountyHunter",
                    "isCampusExpert",
                    "isDeveloperProgramMember",
                    "isEmployee",
                    "isGitHubStar",
                    "isHireable",
                    "isSiteAdmin",
                    QueryNode("watching", fields=["totalCount"]),
                    QueryNode("starredRepositories", fields=["totalCount"]),
                    QueryNode("following", fields=["totalCount"]),
                    QueryNode("followers", fields=["totalCount"]),
                    QueryNode("gists", fields=["totalCount"]),
                    QueryNode("gistComments", fields=["totalCount"]),
                    QueryNode("issueComments", fields=["totalCount"]),
                    QueryNode("issues", fields=["totalCount"]),
                    QueryNode("projects", fields=["totalCount"]),
                    QueryNode("pullRequests", fields=["totalCount"]),
                    QueryNode("repositories", fields=["totalCount"]),
                    QueryNode("repositoryDiscussionComments", fields=["totalCount"]),
                    QueryNode("repositoryDiscussions", fields=["totalCount"]),
                ]
            )
        ]
    )
