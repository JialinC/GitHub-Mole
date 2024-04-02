"""The module defines UserProfileStats that formulate GraphQL query string to extract user profile information 
for a given GitHub ID."""

from typing import Dict, Any
from backend.app.services.github_query.github_graphql.query import QueryNode, Query


class UserProfileStats(Query):
    """
    UserProfileStats is a subclass of Query specifically designed to fetch detailed statistical information
    about a GitHub user's profile using the 'user' field in a GraphQL query.
    """

    def __init__(self) -> None:
        """
        Initializes a UserProfileStats query object to fetch a comprehensive set of information
        about a user, including their activities, contributions, and public profile details.
        """
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
                        # Various boolean fields indicating the user's status or roles:
                        "isBountyHunter",
                        "isCampusExpert",
                        "isDeveloperProgramMember",
                        "isEmployee",
                        "isGitHubStar",
                        "isHireable",
                        "isSiteAdmin",
                        # Nodes representing counts of various items related to the user:
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
                        QueryNode(
                            "repositoryDiscussionComments", fields=["totalCount"]
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def profile_stats(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes the raw data returned from a GraphQL query about a user's profile
        and extracts specific statistics. It formats the data into a more
        accessible and simplified dictionary structure.

        Args:
            raw_data (dict): The raw data returned by the query,
            expected to contain a 'user' key with nested user information.

        Returns:
            dict: A dictionary containing key statistics and information about the user, such as
            their login, creation date, company, number of followers, etc.
            Each piece of information is extracted from the nested structure of the
            input and presented as a flat dictionary for easier access.
        """
        profile_stats = raw_data["user"]
        processed_stats = {
            "github": profile_stats["login"],
            "created_at": profile_stats["createdAt"],
            "company": profile_stats["company"],
            "followers": profile_stats["followers"]["totalCount"],
            "gists": profile_stats["gists"]["totalCount"],
            "issues": profile_stats["issues"]["totalCount"],
            "projects": profile_stats["projects"]["totalCount"],
            "pull_requests": profile_stats["pullRequests"]["totalCount"],
            "repositories": profile_stats["repositories"]["totalCount"],
            "repository_discussions": profile_stats["repositoryDiscussions"][
                "totalCount"
            ],
            "gist_comments": profile_stats["gistComments"]["totalCount"],
            "issue_comments": profile_stats["issueComments"]["totalCount"],
            "commit_comments": profile_stats["commitComments"]["totalCount"],
            "repository_discussion_comments": profile_stats[
                "repositoryDiscussionComments"
            ]["totalCount"],
            "watching": profile_stats["watching"]["totalCount"],
            "starred_repositories": profile_stats["starredRepositories"]["totalCount"],
            "following": profile_stats["following"]["totalCount"],
        }
        return processed_stats
