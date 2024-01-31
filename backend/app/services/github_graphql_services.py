from flask import session
# Import client, exceptions, and authentication classes
from backend.app.services.github_query.github_graphql.client import Client, QueryFailedException
from backend.app.services.github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
# Import query classes
from backend.app.services.github_query.queries.profiles.user_login import UserLoginViewer, UserLogin



# from datetime import datetime, timedelta
# import pandas as pd
# from collections import Counter
# import backend.app.services.github_query.utils.helper as helper
# 
# # all queries
# # utility
# from backend.app.services.github_query.queries.costs.query_cost import QueryCost
# from backend.app.services.github_query.queries.costs.rate_limit import RateLimit
# # user profiles

# from backend.app.services.github_query.queries.profiles.user_profile_stats import UserProfileStats
# # user contribution
# from backend.app.services.github_query.queries.contributions.user_gists import UserGists
# from backend.app.services.github_query.queries.contributions.user_issues import UserIssues
# from backend.app.services.github_query.queries.contributions.user_pull_requests import UserPullRequests
# from backend.app.services.github_query.queries.contributions.user_repositories import UserRepositories
# from backend.app.services.github_query.queries.contributions.user_repository_discussions import UserRepositoryDiscussions
# # user comments
# from backend.app.services.github_query.queries.comments.user_commit_comments import UserCommitComments
# from backend.app.services.github_query.queries.comments.user_gist_comments import UserGistComments
# from backend.app.services.github_query.queries.comments.user_issue_comments import UserIssueComments
# from backend.app.services.github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments
# # time range
# from backend.app.services.github_query.queries.time_range_contributions.user_contributions_collection import UserContributionsCollection
# # repo query
# from backend.app.services.github_query.queries.repositories.repository_commits import RepositoryCommits
# from backend.app.services.github_query.queries.repositories.repository_contributors import RepositoryContributors
# from backend.app.services.github_query.queries.repositories.repository_contributors_contribution import RepositoryContributorsContribution

def get_current_user_login():
    """
    Fetches the login information of the current authenticated user using the OAuth access token.
    
    Returns:
        dict: A dictionary containing the current user's login information, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get('access_token')
    if not token:
        return {"error": "User not authenticated"}
    
    # Initialize the GraphQL client with the OAuth access token
    client = Client(token=token)

    try:
        query = UserLoginViewer()
        response = client.execute(query)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}

def get_specific_user_login(username: str):
    """
    Fetches the login and profile information of a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the specified user's login and profile information.
    """
    query = UserLogin()
    client = Client(authenticator=PersonalAccessTokenAuthenticator(token="your_token_here"))

    try:
        response = client.execute(query, substitutions={"user": username})
        return response
    except QueryFailedException as e:
        return {"error": str(e)}
