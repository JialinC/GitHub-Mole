from python_github_query.github_graphql.query import QueryNode, Query


class UserProfileStats(Query):
    def __init__(self):
        super().__init__(
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
                        QueryNode("issues", fields=["totalCount"]),
                        QueryNode("projects", fields=["totalCount"]),
                        QueryNode("pullRequests", fields=["totalCount"]),
                        QueryNode("repositories", fields=["totalCount"]),
                        QueryNode("repositoryDiscussions", fields=["totalCount"]),
                        QueryNode("gistComments", fields=["totalCount"]),
                        QueryNode("issueComments", fields=["totalCount"]),
                        QueryNode("commitComments", fields=["totalCount"]),
                        QueryNode("repositoryDiscussionComments", fields=["totalCount"]),
                    ]
                )
            ]
        )

    @staticmethod
    def profile_stats(profile_stats: dict):
        """
        Return the contributors contribution collection
        Args:
            profile_stats: the raw data returned by the query
        Returns:
        """
        raw_data = profile_stats["user"]
        profile_stats = {"github": raw_data["login"],
                         "created_at": raw_data["createdAt"],
                         "company": raw_data["company"],
                         "followers": raw_data["followers"]["totalCount"],
                         "gists": raw_data["gists"]["totalCount"],
                         "issues": raw_data["issues"]["totalCount"],
                         "projects": raw_data["projects"]["totalCount"],
                         "pull_requests": raw_data["pullRequests"]["totalCount"],
                         "repositories": raw_data["repositories"]["totalCount"],
                         "repository_discussions": raw_data["repositoryDiscussions"]["totalCount"],
                         "gist_comments": raw_data["gistComments"]["totalCount"],
                         "issue_comments": raw_data["issueComments"]["totalCount"],
                         "commit_comments": raw_data["commitComments"]["totalCount"],
                         "repository_discussion_comments": raw_data["repositoryDiscussionComments"]["totalCount"]}
        return profile_stats

