"""
This module provides services for interacting with the GitHub GraphQL API.
It includes functions to initialize a GitHub GraphQL client and fetch various
types of data related to GitHub users and repositories, such as rate limits,
user login information, profile statistics, contributions, repositories, comments,
and more.

Functions:
    get_github_client(token: str, protocol: str = "https", host: str = "api.github.com") -> Client:
    get_rate_limit(protocol: str, host: str, token: str) -> dict:
    get_current_user_login(protocol: str, host: str, token: str) -> dict:
    get_specific_user_login(login: str, protocol: str, host: str, token: str) -> dict:
    get_user_profile_stats(login: str, protocol: str, host: str, token: str) -> dict:
    get_user_contributions_collection(login: str, protocol: str, host: str, token: str, start: str = None, end: str = None) -> dict:
    get_user_contribution_years(login: str, protocol: str, host: str, token: str) -> dict:
    get_user_contribution_calendar(login: str, protocol: str, host: str, token: str, start: str = None, end: str = None) -> dict:
    get_user_repositories_page(login: str, protocol: str, host: str, token: str, repo_t: str, end_cursor: Optional[str] = None) -> dict:
    get_user_commit_comments_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_user_gist_comments_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_user_issue_comments_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_user_repository_discussion_comments_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_user_gists_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_user_issues_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_user_pull_requests_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_user_repository_discussions_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_repository_branches_page(owner: str, repo_name: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_repository_default_branch(owner: str, repo_name: str, protocol: str, host: str, token: str) -> dict:
    get_repository_contributors_page(owner: str, repo_name: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_repository_branch_commits_page(owner: str, repo_name: str, branch_name: str, use_default: bool, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> Dict[str, Any]:
    get_user_repository_names_page(login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
    get_repository_contributor_contributions_page(owner: str, repo_name: str, branch_name: str, id: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None) -> dict:
"""

from datetime import datetime

from typing import Dict, Any, Optional
from collections import Counter
from app.services.github_query.utils.helper import add_by_days
from app.services.github_query.queries import (
    RateLimit,
    UserLoginViewer,
    UserLogin,
    UserProfileStats,
    UserContributionsCollection,
    UserContributionCalendar,
    UserCommitComments,
    UserGistComments,
    UserIssueComments,
    UserRepositoryDiscussionComments,
    UserGists,
    UserIssues,
    UserPullRequests,
    UserRepositories,
    UserRepositoryDiscussions,
    RepositoryContributors,
    RepositoryBranches,
    RepositoryBranchCommits,
    RepositoryDefaultBranch,
    RepositoryContributorContributions,
    UserRepositoryNames,
)
from .github_query.graphql_client import (
    PersonalAccessTokenAuthenticator,
    QueryFailedException,
    Client,
)


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


def get_rate_limit(protocol: str, host: str, token: str):
    """
    Fetches the current API rate limit status for the authenticated GitHub user.

    Args:
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.

    Returns:
        dict: A dictionary containing the rate limit details or an error message.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=RateLimit(dryrun=True))
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_current_user_login(protocol: str, host: str, token: str):
    """
    Fetches the current authenticated user's login information using GraphQL.

    Args:
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.

    Returns:
        dict: A dictionary containing the login details or an error message.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=UserLoginViewer())
        if "no_limit" in response:
            return response
        return UserLoginViewer.profile_stats(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_specific_user_login(login: str, protocol: str, host: str, token: str):
    """
    Fetches the login and profile information of a specific user.

    Args:
        login (str): The GitHub username of the user.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.

    Returns:
        dict: A dictionary containing the specified user's login and profile information.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=UserLogin(login=login))
        if "no_limit" in response:
            return response
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_profile_stats(login: str, protocol: str, host: str, token: str):
    """
    Fetches the profile statistics of a specific GitHub user.

    Args:
        login (str): The GitHub username of the user.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.

    Returns:
        dict: A dictionary containing the user's profile statistics.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=UserProfileStats(login=login))
        if "no_limit" in response:
            return response
        return UserProfileStats.profile_stats(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_contributions_collection(
    login: str, protocol: str, host: str, token: str, start: str = None, end: str = None
):
    """
    Retrieves a user's GitHub contributions over a specific time range.

    Args:
        login (str): GitHub username.
        protocol (str): HTTP/HTTPS protocol for GitHub API.
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token (PAT) for authentication.
        start (str, optional): Start date (YYYY-MM-DD). Defaults to account creation date.
        end (str, optional): End date (YYYY-MM-DD). Defaults to the current date.

    Returns:
        dict: Contribution statistics as a dictionary with counts for commits, PRs, issues, etc.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """

    # Fetch user details to determine the account creation date
    response = get_specific_user_login(login, protocol, host, token)
    if "no_limit" in response:
        return response  # Rate limit reached, return rate-limit response

    created_at = response["user"]["createdAt"]
    client = get_github_client(protocol=protocol, host=host, token=token)

    # Convert start and end dates to datetime format
    gh_start = (
        datetime.strptime(start, "%Y-%m-%d")
        if start
        else datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    )
    gh_end = datetime.strptime(end, "%Y-%m-%d") if end else datetime.now()
    end = gh_end.strftime("%Y-%m-%dT%H:%M:%SZ")
    start = gh_start.strftime("%Y-%m-%dT%H:%M:%SZ")

    contributions = Counter({"res_con": 0, "commit": 0, "pr_review": 0})
    period_end = add_by_days(start, 365)

    try:
        while start < end:
            if period_end > end:
                period_end = end

            response = client.execute(
                query=UserContributionsCollection(
                    login=login, start=f'"{start}"', end=f'"{period_end}"'
                )
            )
            if "no_limit" in response:
                return response
            queried_contribution = (
                UserContributionsCollection.user_contributions_collection(response)
            )
            for key in contributions:
                contributions[key] += queried_contribution[key]
            start = period_end
            period_end = add_by_days(start, 365)
        return contributions
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_contribution_years(login: str, protocol: str, host: str, token: str):
    """
    Fetches the contribution years of a specific GitHub user.

    Args:
        login (str): The GitHub username of the user.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.

    Returns:
        dict: A list containing the years in which the user has contributed.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        response = client.execute(query=UserContributionCalendar(login=login))
        if "no_limit" in response:
            return response
        _, _, years = UserContributionCalendar.user_contribution_calendar(response)
        return years
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_contribution_calendar(
    login: str, protocol: str, host: str, token: str, start: str = None, end: str = None
):
    """
    Fetches the contribution calendar of a specific GitHub user.

    Args:
        login (str): The GitHub username.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.
        start (str, optional): Start date for filtering contributions.
        end (str, optional): End date for filtering contributions.

    Returns:
        dict: Contribution calendar containing dates and contribution counts.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    query_args = {"login": login}
    if start:
        query_args["start"] = f'"{start}"'
    if end:
        query_args["end"] = f'"{end}"'
    try:
        response = client.execute(query=UserContributionCalendar(**query_args))
        if "no_limit" in response:
            return response
        join_date, calendar, _ = UserContributionCalendar.user_contribution_calendar(
            response
        )
        return join_date, calendar
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repositories_page(
    login: str,
    protocol: str,
    host: str,
    token: str,
    repo_t: str,
    end_cursor: Optional[str] = None,
):
    """
    Fetches a page of repositories for a specified GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        repo_t (str): Repository type (A, B, C, D).
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing repository data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    is_fork = None
    ownership = None
    if repo_t == "A":
        is_fork = False
        ownership = "[OWNER]"
    elif repo_t == "B":
        is_fork = True
        ownership = "[OWNER]"
    elif repo_t == "C":
        is_fork = False
        ownership = "[COLLABORATOR]"
    else:
        is_fork = True
        ownership = "[COLLABORATOR]"
    try:
        response = client.execute(
            query=UserRepositories(login=login, is_fork=is_fork, ownership=ownership),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserRepositories.user_repository_page(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_commit_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of commit comments for a specified GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing commit comment data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserCommitComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserCommitComments.user_commit_comments(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_gist_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of gist comments for a specified GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing gist comment data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserGistComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserGistComments.user_gist_comments(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_issue_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of issue comments for a specified GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing issue comment data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserIssueComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserIssueComments.user_issue_comments(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repository_discussion_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of repository discussion comments for a specified GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing repository discussion comment data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserRepositoryDiscussionComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserRepositoryDiscussionComments.user_repository_discussion_comments(
            response
        )
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_gists_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of gists created by a specific GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing gists data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserGists(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserGists.user_gists(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_issues_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of issues created by or assigned to a specific GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing issues data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserIssues(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserIssues.user_issues(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_pull_requests_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of pull requests created by or assigned to a specific GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing pull request data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserPullRequests(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserPullRequests.user_pull_requests(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repository_discussions_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Fetches a page of repository discussions for a specified GitHub user.

    Args:
        login (str): GitHub username.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing repository discussion data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserRepositoryDiscussions(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return UserRepositoryDiscussions.user_repository_discussions(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_repository_branches_page(
    owner: str,
    repo_name: str,
    protocol: str,
    host: str,
    token: str,
    end_cursor: Optional[str] = None,
):
    """
    Fetches a page of branches for a given repository.

    Args:
        owner (str): The GitHub username or organization that owns the repository.
        repo_name (str): The repository name.
        protocol (str): API protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): User’s GitHub OAuth token.
        end_cursor (Optional[str]): Cursor for paginated results.

    Returns:
        dict: A dictionary containing branch data and pagination info.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        response = client.execute(
            query=RepositoryBranches(owner=owner, repo_name=repo_name),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return RepositoryBranches.branches(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_repository_default_branch(
    owner: str,
    repo_name: str,
    protocol: str,
    host: str,
    token: str,
):
    """
    Fetches the default branch of a GitHub repository.

    Args:
        owner (str): The GitHub username or organization name.
        repo_name (str): The name of the repository.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.

    Returns:
        dict: The default branch of the repository.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        response = client.execute(
            query=RepositoryDefaultBranch(owner=owner, repo_name=repo_name)
        )
        if "no_limit" in response:
            return response
        return RepositoryDefaultBranch.default_branch(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_repository_contributors_page(
    owner: str,
    repo_name: str,
    protocol: str,
    host: str,
    token: str,
    end_cursor: Optional[str] = None,
):
    """
    Fetches the list of contributors of a GitHub repository.

    Args:
        owner (str): The GitHub username or organization name.
        repo_name (str): The name of the repository.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        dict: A list of contributors including their GitHub login, name, and email.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=RepositoryContributors(owner=owner, repo_name=repo_name),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_repository_branch_commits_page(
    owner: str,
    repo_name: str,
    branch_name: str,
    use_default: bool,
    protocol: str,
    host: str,
    token: str,
    end_cursor: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetches commit history for a specific branch of a GitHub repository.

    Args:
        owner (str): The GitHub username or organization name.
        repo_name (str): The repository name.
        branch_name (str): The branch name (ignored if use_default=True).
        use_default (bool): Whether to fetch from the default branch.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token.
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        dict: Contains pagination info and commit SHAs.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        query = RepositoryBranchCommits(
            owner=owner,
            repo_name=repo_name,
            branch_name=branch_name,
            use_default=use_default,
        )
        response = client.execute(
            query=query,
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        history = query.commits_list(response)
        page_info = history["pageInfo"]
        commits = history["nodes"]
        return {"pageInfo": page_info, "commits": commits}
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repository_names_page(
    login: str,
    protocol: str,
    host: str,
    token: str,
    end_cursor: Optional[str] = None,
):
    """
    Fetches names of all repositories owned by a GitHub user.

    Args:
        login (str): The GitHub username.
        protocol (str): The protocol (http/https).
        host (str): GitHub API host (e.g., api.github.com).
        token (str): GitHub personal access token for authentication.
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        dict: Contains pagination info, repository names, and GitHub user ID.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        response = client.execute(
            query=UserRepositoryNames(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        repos, ghid = UserRepositoryNames.user_repository_names(response)
        page_info = repos["pageInfo"]
        nodes = repos["nodes"]
        return {"pageInfo": page_info, "repos": nodes, "id": ghid}
    except QueryFailedException as e:
        return {"error": str(e)}


def get_repository_contributor_contributions_page(
    owner: str,
    repo_name: str,
    branch_name: str,
    id: str,
    protocol: str,
    host: str,
    token: str,
    end_cursor: Optional[str] = None,
):
    """
    Fetches contributions made by a specific contributor to a repository.

    Args:
        owner (str): Repository owner.
        repo_name (str): Repository name.
        branch_name (str): Branch name.
        id (str): GitHub username of the contributor.
        protocol (str): API protocol (http/https).
        host (str): API host (e.g., api.github.com).
        token (str): GitHub access token for authentication.
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        dict: Contains pagination info and commit history.

    Raises:
        QueryFailedException: If the GraphQL query execution fails.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=RepositoryContributorContributions(
                owner=owner,
                repo_name=repo_name,
                branch_name=branch_name,
                github_id=id,
            ),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        if "no_limit" in response:
            return response
        history = RepositoryContributorContributions.commits_list(response)
        page_info = history["pageInfo"]
        commits = history["nodes"]
        return {"pageInfo": page_info, "commits": commits}
    except QueryFailedException as e:
        return {"error": str(e)}
