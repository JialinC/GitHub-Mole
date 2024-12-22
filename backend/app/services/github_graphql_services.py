from typing import Dict, Any, Optional

from .github_query.graphql_client import (
    PersonalAccessTokenAuthenticator,
    QueryFailedException,
    Client,
)

from backend.app.services.github_query.queries import (
    UserLoginViewer,
    UserLogin,
)

from .github_query.queries.comments import UserCommitComments

# from .github_query.queries.repositories import (
#     RepositoryContributors,
#     RepositoryContributorsContribution,
#     RepositoryCommits,
# )


def get_github_client(
    token: str, protocol: str = "https", host: str = "api.github.com"
) -> Client:
    """
    Initializes and returns a GitHub GraphQL client.

    Args:
        token (str): The OAuth access token.

    Returns:
        Client: An initialized GitHub GraphQL client.
    """
    return Client(
        protocol=protocol,
        host=host,
        is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=token),
    )


def get_current_user_login(protocol: str, host: str, token: str):
    """
    Fetches the login information of the current authenticated user using the OAuth access token.

    Returns:
        dict: A dictionary containing the current user's login information, or an error message.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=UserLoginViewer())
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_specific_user_login(login: str, protocol: str, host: str, token: str):
    """
    Fetches the login and profile information of a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the specified user's login and profile information.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=UserLogin(login=login))
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


# def get_repository_contributors(
#     owner: str, repo_name: str, page_size: int = 100, token: Optional[str] = None
# ):
#     """
#     Fetches contributors for a specific repository.
#     """
#     auth_token = token
#     if not auth_token:
#         return {"error": "User not authenticated"}

#     client = get_github_client(token)

#     try:
#         query = RepositoryContributors(
#             owner=owner, repo_name=repo_name, pg_size=page_size
#         )
#         paginated_data = client.execute(query=query)
#         authors = set()
#         for page in paginated_data:
#             curr_authors = query.extract_unique_author(page)
#             for author in curr_authors:
#                 authors.add(author)
#         return list(authors)
#     except QueryFailedException as e:
#         return {"error": str(e)}


# def get_contributor_contributions(
#     owner: str,
#     repo_name: str,
#     contributor_id: str,
#     page_size: int = 100,
#     token: Optional[str] = None,
# ):
#     """
#     Fetches contributions made by a specific contributor to a repository.
#     """
#     auth_token = token
#     if not auth_token:
#         return {"error": "User not authenticated"}

#     client = Client(
#         host="api.github.com",
#         is_enterprise=False,
#         authenticator=PersonalAccessTokenAuthenticator(token=auth_token),
#     )

#     contributor = {"id": contributor_id}

#     try:
#         query = RepositoryContributorsContribution(
#             owner, repo_name, contributor, page_size
#         )
#         # Execute query and handle pagination
#         response = client.execute(query=query)
#         all_commits = []
#         for page in response:
#             all_commits = query.user_cumulated_contribution(page)
#             break
#         return all_commits
#     except QueryFailedException as e:
#         return {"error": str(e)}


# def get_repository_commits(
#     owner: str, repo_name: str, page_size: int = 100, token: Optional[str] = None
# ) -> Dict[str, Any]:
#     """
#     Fetches commits for a specific repository.
#     """
#     auth_token = token
#     if not auth_token:
#         return {"error": "User not authenticated"}

#     client = Client(
#         host="api.github.com",
#         is_enterprise=False,
#         authenticator=PersonalAccessTokenAuthenticator(token=auth_token),
#     )

#     try:
#         query = RepositoryCommits(owner=owner, repo_name=repo_name, pg_size=page_size)
#         # Execute query and handle pagination
#         paginated_data = client.execute(query=query)
#         all_commits = []
#         for page in paginated_data:
#             all_commits = query.commits_list(page)
#             break
#         return all_commits

#     except QueryFailedException as e:
#         return {"error": str(e)}
