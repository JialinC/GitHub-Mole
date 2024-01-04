from collections import Counter
from backend.app.services.github_query.github_graphql.query import QueryNode, Query

class UserContributionsCollection(Query):
    """
    UserContributionsCollection is a subclass of Query specifically designed to fetch a GitHub user's contributions
    over a certain period. It includes detailed contribution counts like commits, issues, pull requests, etc.
    """
    
    def __init__(self) -> None:
        """
        Initializes a UserContributionsCollection query object to fetch detailed contribution information of a user.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},  # The GitHub username for which to fetch contribution data.
                    fields=[
                        QueryNode(
                            "contributionsCollection",
                            args={"from": "$start", "to": "$end"},  # Time period for the contributions.
                            fields=[
                                "startedAt",  # The date and time at which the collection period starts.
                                "endedAt",    # The date and time at which the collection period ends.
                                "restrictedContributionsCount",  # Count of contributions to private repos the viewer does not have access to.
                                "totalCommitContributions",  # The total number of commits authored by the user.
                                "totalIssueContributions",  # The total number of issues opened by the user.
                                "totalPullRequestContributions",  # The total number of pull requests opened by the user.
                                "totalPullRequestReviewContributions",  # The total number of pull request reviews by the user.
                                "totalRepositoryContributions"  # The total number of repositories the user contributed to.
                                # Each of these fields provides a count related to different types of contributions.
                                # User can extend this to include fields they interested. 
                            ]
                        ),
                    ]
                )
            ]
        )

    @staticmethod
    def user_contributions_collection(cumulated_contributions_collection: dict) -> Counter:
        """
        Processes the raw data returned from a GraphQL query about a user's contributions collection
        and aggregates the various types of contributions into a countable collection.

        Args:
            cumulated_contributions_collection (dict): The raw data returned by the query, 
                                                      expected to contain nested contribution counts.

        Returns:
            Counter: A collection counter aggregating the various types of contributions made by the user.
        """
        raw_data = cumulated_contributions_collection["user"]["contributionsCollection"]
        contribution_collection = Counter({
            "res_con": raw_data["restrictedContributionsCount"],  # Restricted contributions count.
            "commit": raw_data["totalCommitContributions"],  # Total commit contributions.
            "issue": raw_data["totalIssueContributions"],  # Total issue contributions.
            "pr": raw_data["totalPullRequestContributions"],  # Total pull request contributions.
            "pr_review": raw_data["totalPullRequestReviewContributions"],  # Total pull request review contributions.
            "repository": raw_data["totalRepositoryContributions"]  # Total repository contributions.
        })
        return contribution_collection
