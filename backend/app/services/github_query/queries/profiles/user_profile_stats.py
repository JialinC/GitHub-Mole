from backend.app.services.github_query.github_graphql.query import QueryNode, Query

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
        Processes the raw data returned from a GraphQL query about a user's profile 
        and extracts specific statistics. It formats the data into a more 
        accessible and simplified dictionary structure.

        Args:
            profile_stats (dict): The raw data returned by the query, 
                                expected to contain a 'user' key with nested user information.

        Returns:
            dict: A dictionary containing key statistics and information about the user, such as
                their login, creation date, company, number of followers, etc.
                Each piece of information is extracted from the nested structure of the 
                input and presented as a flat dictionary for easier access.
        """
        raw_data = profile_stats["user"]
        processed_stats = {
            "github": raw_data["login"],
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
            "repository_discussion_comments": raw_data["repositoryDiscussionComments"]["totalCount"],
            "watching": raw_data["watching"]["totalCount"],
            "starred_repositories": raw_data["starredRepositories"]["totalCount"],
            "following": raw_data["following"]["totalCount"]
        }
        return processed_stats

