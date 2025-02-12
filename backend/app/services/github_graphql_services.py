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
    Fetches the login information of the current authenticated user using the OAuth access token.

    Returns:
        dict: A dictionary containing the current user's login information, or an error message.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=RateLimit(dryrun=True))
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_current_user_login(protocol: str, host: str, token: str):
    """
    Fetches the login information of the current authenticated user using the OAuth access token.

    Returns:
        dict: A dictionary containing the current user's login information, or an error message.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=UserLoginViewer())
        return UserLoginViewer.profile_stats(response)
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
        print(response)
        return response
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_profile_stats(login: str, protocol: str, host: str, token: str):
    """ """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(query=UserProfileStats(login=login))
        return UserProfileStats.profile_stats(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_contributions_collection(
    login: str, protocol: str, host: str, token: str, start: str = None, end: str = None
):
    """ """
    response = get_specific_user_login(login, protocol, host, token)
    created_at = response["user"]["createdAt"]
    client = get_github_client(protocol=protocol, host=host, token=token)
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
    """ """
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        response = client.execute(query=UserContributionCalendar(login=login))
        _, _, years = UserContributionCalendar.user_contribution_calendar(response)
        return years
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_contribution_calendar(
    login: str, protocol: str, host: str, token: str, start: str = None, end: str = None
):
    """ """
    client = get_github_client(protocol=protocol, host=host, token=token)
    query_args = {"login": login}
    if start:
        query_args["start"] = f'"{start}"'
    if end:
        query_args["end"] = f'"{end}"'
    try:
        response = client.execute(query=UserContributionCalendar(**query_args))
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
    Args:
    Returns:
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
        return UserRepositories.user_repository_page(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_commit_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserCommitComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return UserCommitComments.user_commit_comments(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_gist_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserGistComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return UserGistComments.user_gist_comments(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_issue_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserIssueComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return UserIssueComments.user_issue_comments(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repository_discussion_comments_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserRepositoryDiscussionComments(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return UserRepositoryDiscussionComments.user_repository_discussion_comments(
            response
        )
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_gists_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserGists(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return UserGists.user_gists(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_issues_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserIssues(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return UserIssues.user_issues(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_pull_requests_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserPullRequests(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return UserPullRequests.user_pull_requests(response)
    except QueryFailedException as e:
        return {"error": str(e)}


def get_user_repository_discussions_page(
    login: str, protocol: str, host: str, token: str, end_cursor: Optional[str] = None
):
    """
    Args:
    Returns:
    """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=UserRepositoryDiscussions(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
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
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        response = client.execute(
            query=RepositoryBranches(owner=owner, repo_name=repo_name),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        return RepositoryBranches.branches(response)
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
    """ """
    client = get_github_client(protocol=protocol, host=host, token=token)

    try:
        response = client.execute(
            query=RepositoryContributors(owner=owner, repo_name=repo_name),
            pagination="frontend",
            end_cursor=end_cursor,
        )
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
    Fetches commits for a specific repository.
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
        history = query.commits_list(response)
        page_info = history["pageInfo"]
        commits = history["nodes"]
        return {"pageInfo": page_info, "commits": commits}
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

        history = RepositoryContributorContributions.commits_list(response)
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
    Fetches names of all the repos of a given GitHub login.
    """
    client = get_github_client(protocol=protocol, host=host, token=token)
    try:
        response = client.execute(
            query=UserRepositoryNames(login=login),
            pagination="frontend",
            end_cursor=end_cursor,
        )
        repos, ghid = UserRepositoryNames.user_repository_names(response)
        page_info = repos["pageInfo"]
        nodes = repos["nodes"]
        return {"pageInfo": page_info, "repos": nodes, "id": ghid}
    except QueryFailedException as e:
        return {"error": str(e)}
