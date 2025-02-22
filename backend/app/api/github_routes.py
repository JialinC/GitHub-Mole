"""
This module defines the GitHub GraphQL API routes for the backend application.

It includes various endpoints to fetch data from GitHub using GraphQL queries and REST API calls.
The routes are protected with JWT authentication and require a valid JWT token to access.

Routes:
    - /graphql/rate-limit: Fetches the current API rate limit usage for the authenticated GitHub user.
    - /graphql/current-user-login: Fetches the login details of the currently authenticated GitHub user.
    - /graphql/user-login/<login>: Fetches the login details of a specific GitHub user identified by their username.
    - /graphql/user-profile-stats/<login>: Fetches the profile statistics of a specific GitHub user.
    - /graphql/user-contributions-collection/<login>: Fetches a user's GitHub contributions over a specified period.
    - /graphql/user-contribution-years/<login>: Fetches the years in which a GitHub user has made contributions.
    - /graphql/user-contribution-calendar/<login>: Fetches a user's contribution calendar within a specified date range.
    - /graphql/user-repositories-a/<login>: Fetches non-forked repositories owned by the specified GitHub user.
    - /graphql/user-repositories-b/<login>: Fetches forked repositories owned by the specified GitHub user.
    - /graphql/user-repositories-c/<login>: Fetches non-forked repositories where a GitHub user is a collaborator.
    - /graphql/user-repositories-d/<login>: Fetches forked repositories where a GitHub user is a collaborator.
    - /graphql/user-commit-comments/<login>: Fetches commit comments made by a specified GitHub user.
    - /graphql/user-gist-comments/<login>: Fetches gist comments made by a specified GitHub user.
    - /graphql/user-issue-comments/<login>: Fetches issue comments made by a specified GitHub user.
    - /graphql/user-repository-discussion-comments/<login>: Fetches discussion comments made by a specified GitHub user
       in repository discussions.
    - /graphql/user-gists/<login>: Fetches gists created by a specified GitHub user.
    - /graphql/user-issues/<login>: Fetches issues created by or assigned to a specified GitHub user.
    - /graphql/user-pull-requests/<login>: Fetches pull requests created by or assigned to a specified GitHub user.
    - /graphql/user-repository-discussions/<login>: Fetches repository discussions associated with a specific GitHub
      user.
    - /graphql/repository_branches/<owner>/<repo>: Fetches repository branches for a specified GitHub repository.
    - /graphql/repository_default_branch/<owner>/<repo>: Fetches the default branch of a GitHub repository.
    - /graphql/repository_contributors/<owner>/<repo>: Fetches the contributors of a GitHub repository.
    - /graphql/repository_branch_commits/<owner>/<repo>/<use_default>: Fetches commit history for a specific branch in
      a GitHub repository.
    - /graphql/user_repository_names/<login>: Fetches the names of all repositories owned by a given GitHub user.
    - /graphql/repository_contributor_contributions/<owner>/<repo>/<login>: Fetches commit contributions of a GitHub
      user in a specific repository.
    - /rest/commits/<owner>/<repo>/<sha>: Fetches details of a specific commit from GitHub.

Helper Functions:
    - check_user: Checks if the authenticated user exists in the database.
    - extract_user_credentials_and_host: Extracts the user's personal access token, protocol, and host from the user
      object.
    - fetch_with_retries: Fetches data with retry logic and exponential backoff.

Constants:
    - MAX_RETRIES: Maximum number of retry attempts for fetching data.
    - INITIAL_RETRY_DELAY: Initial delay in seconds before retrying a failed request.
"""

import logging
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from requests.exceptions import Timeout, RequestException
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.special import TextLexer

from app.models.user import User
from ..services.github_graphql_services import (
    get_rate_limit,
    get_current_user_login,
    get_specific_user_login,
    get_user_profile_stats,
    get_user_contributions_collection,
    get_user_contribution_years,
    get_user_contribution_calendar,
    get_user_repositories_page,
    get_user_commit_comments_page,
    get_user_gist_comments_page,
    get_user_issue_comments_page,
    get_user_repository_discussion_comments_page,
    get_user_gists_page,
    get_user_issues_page,
    get_user_pull_requests_page,
    get_user_repository_discussions_page,
    get_repository_branches_page,
    get_repository_default_branch,
    get_repository_contributors_page,
    get_repository_branch_commits_page,
    get_repository_contributor_contributions_page,
    get_user_repository_names_page,
)

github_bp = Blueprint("api", __name__)


def check_user():
    """
    Check if the user exists in the database based on the GitHub ID obtained from the JWT token.

    Returns:
        user (User): The user object if found.
        Response: A JSON response with an error message and a 404 status code if the user is not found.
    """
    github_id = get_jwt_identity()
    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        logging.error("User with GitHub ID %s not found", github_id)
        return jsonify({"msg": "User not found"}), 404
    return user


def extract_user_credentials_and_host(user):
    """
    Extracts the personal access token, protocol, and host from a user's API URL.

    Args:
        user (object): An object containing user information, including 'personal_access_token' and 'api_url'.

    Returns:
        tuple: A tuple containing the personal access token (str), protocol (str), and host (str).
    """
    pat = user.personal_access_token
    parsed_url = urlparse(user.api_url)
    protocol = parsed_url.scheme
    host = parsed_url.netloc
    return pat, protocol, host


@github_bp.route("/graphql/rate-limit", methods=["GET"])
@jwt_required()
def rate_limit():
    """
    Fetches the current API rate limit usage for the authenticated GitHub user.

    Returns:
        Response (JSON): A dictionary containing the current rate limit details.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        500 Internal Server Error: If an unexpected error occurs.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_rate_limit(protocol=protocol, host=host, token=pat)
    return jsonify(data)


@github_bp.route("/graphql/current-user-login", methods=["GET"])
@jwt_required()
def current_user_login():
    """
    Fetches the login details of the currently authenticated GitHub user.

    Returns:
        Response (JSON): A dictionary containing the current user's GitHub login information.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        500 Internal Server Error: If an unexpected error occurs.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_current_user_login(protocol=protocol, host=host, token=pat)
    return jsonify(data)


@github_bp.route("/graphql/user-login/<login>", methods=["GET"])
@jwt_required()
def specific_user_login(login):
    """
    Fetches the login details of a specific GitHub user identified by their username.

    URL Parameter:
        login (str): The GitHub username of the user.

    Returns:
        Response (JSON): A dictionary containing the user's GitHub login information.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_specific_user_login(login, protocol, host, pat)
    return jsonify(data)


@github_bp.route("/graphql/user-profile-stats/<login>", methods=["GET"])
@jwt_required()
def user_profile_stats(login):
    """
    Fetches the profile statistics of a specific GitHub user.

    URL Parameter:
        login (str): The GitHub username of the user.

    Returns:
        Response (JSON): A dictionary containing the user's profile statistics.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_profile_stats(login, protocol, host, pat)
    if "error" in data:
        return jsonify({"error": "Not Found", "message": login})

    return jsonify(data)


@github_bp.route("/graphql/user-contributions-collection/<login>", methods=["GET"])
@jwt_required()
def user_contributions_collection(login):
    """
    Fetches a user's GitHub contributions over a specified period.

    Args:
        login (str): GitHub username for which contributions are requested.

    Query Parameters:
        start (str, optional): Start date (YYYY-MM-DD). Defaults to account creation date.
        end (str, optional): End date (YYYY-MM-DD). Defaults to the current date.

    Returns:
        Response (JSON): A dictionary containing the count of different contribution types.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    start = request.args.get("start")
    end = request.args.get("end")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_contributions_collection(login, protocol, host, pat, start, end)
    return jsonify(data)


@github_bp.route("/graphql/user-contribution-years/<login>", methods=["GET"])
@jwt_required()
def user_contribution_years(login):
    """
    Fetches the years in which a GitHub user has made contributions.

    URL Parameter:
        login (str): The GitHub username of the user.

    Returns:
        Response (JSON): A list of years in which the user has contributed.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_contribution_years(login, protocol, host, pat)
    return jsonify(data)


@github_bp.route("/graphql/user-contribution-calendar/<login>", methods=["GET"])
@jwt_required()
def user_contribution_calendar(login):
    """
    Fetches a user's contribution calendar within a specified date range.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        start (str, optional): Start date for the contribution calendar (format: YYYY-MM-DD).
        end (str, optional): End date for the contribution calendar (format: YYYY-MM-DD).

    Returns:
        Response (JSON): Contribution history including activity dates and counts.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    start = request.args.get("start")
    end = request.args.get("end")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_contribution_calendar(login, protocol, host, pat, start, end)
    return jsonify(data)


@github_bp.route("/graphql/user-repositories-a/<login>", methods=["GET"])
@jwt_required()
def user_repositories_a(login):
    """
    Fetches non-forked repositories owned by the specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of repositories owned by the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    repo_t = "A"
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_repositories_page(login, protocol, host, pat, repo_t, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-repositories-b/<login>", methods=["GET"])
@jwt_required()
def user_repositories_b(login):
    """
    Fetches forked repositories owned by the specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of repositories owned by the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    repo_t = "B"
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_repositories_page(login, protocol, host, pat, repo_t, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-repositories-c/<login>", methods=["GET"])
@jwt_required()
def user_repositories_c(login):
    """
    This API endpoint retrieves non-forked repositories where a GitHub user is a collaborator.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of repositories owned by the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    repo_t = "C"
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_repositories_page(login, protocol, host, pat, repo_t, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-repositories-d/<login>", methods=["GET"])
@jwt_required()
def user_repositories_d(login):
    """
    This API endpoint retrieves forked repositories where a GitHub user is a collaborator.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of repositories owned by the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    repo_t = "D"
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_repositories_page(login, protocol, host, pat, repo_t, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-commit-comments/<login>", methods=["GET"])
@jwt_required()
def user_commit_comments(login):
    """
    Fetches commit comments made by a specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of commit comments.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_commit_comments_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-gist-comments/<login>", methods=["GET"])
@jwt_required()
def user_gist_comments(login):
    """
    Fetches gist comments made by a specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of gist comments.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_gist_comments_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-issue-comments/<login>", methods=["GET"])
@jwt_required()
def user_issue_comments(login):
    """
    Fetches issue comments made by a specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of issue comments.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_issue_comments_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route(
    "/graphql/user-repository-discussion-comments/<login>", methods=["GET"]
)
@jwt_required()
def user_repository_discussion_comments(login):
    """
    Fetches discussion comments made by a specified GitHub user in repository discussions.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of repository discussion comments.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_repository_discussion_comments_page(
        login, protocol, host, pat, end_cursor
    )
    return jsonify(data)


@github_bp.route("/graphql/user-gists/<login>", methods=["GET"])
@jwt_required()
def user_gists(login):
    """
    Fetches gists created by a specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of gists created by the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_gists_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-issues/<login>", methods=["GET"])
@jwt_required()
def user_issues(login):
    """
    Fetches issues created by or assigned to a specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of issues associated with the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_issues_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-pull-requests/<login>", methods=["GET"])
@jwt_required()
def user_pull_requests(login):
    """
    Fetches pull requests created by or assigned to a specified GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of pull requests associated with the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_pull_requests_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/user-repository-discussions/<login>", methods=["GET"])
@jwt_required()
def user_repository_discussions(login):
    """
    Fetches repository discussions associated with a specific GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of repository discussions related to the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_repository_discussions_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/repository_branches/<owner>/<repo>", methods=["GET"])
@jwt_required()
def repository_branches(owner, repo):
    """
    Fetches repository branches for a specified GitHub repository.

    URL Parameters:
        owner (str): The GitHub username or organization that owns the repository.
        repo (str): The repository name.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results (default: None).

    Returns:
        Response (JSON): A list of repository branches.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the repository does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_branches_page(owner, repo, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/repository_default_branch/<owner>/<repo>", methods=["GET"])
@jwt_required()
def repository_default_branch(owner, repo):
    """
    Fetches the default branch of a GitHub repository.

    URL Parameters:
        owner (str): The GitHub username or organization name.
        repo (str): The name of the repository.

    Returns:
        Response (JSON): The default branch of the specified repository.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the repository does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_default_branch(owner, repo, protocol, host, pat)
    return jsonify(data)


@github_bp.route("/graphql/repository_contributors/<owner>/<repo>", methods=["GET"])
@jwt_required()
def repository_contributors(owner, repo):
    """
    Fetches the contributors of a GitHub repository.

    URL Parameters:
        owner (str): The GitHub username or organization name.
        repo (str): The name of the repository.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        Response (JSON): A list of contributors including their GitHub login, name, and email.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the repository does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_contributors_page(
        owner, repo, protocol, host, pat, end_cursor
    )
    return jsonify(data)


@github_bp.route(
    "/graphql/repository_branch_commits/<owner>/<repo>/<use_default>", methods=["GET"]
)
@jwt_required()
def repository_branch_commits(owner, repo, use_default):
    """
    Fetches commit history for a specific branch in a GitHub repository.

    URL Parameters:
        owner (str): The GitHub username or organization name.
        repo (str): The name of the repository.
        use_default (bool): Whether to use the default branch.

    Query Parameters:
        branch (str, optional): The name of the branch. Required if use_default is False.
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        Response (JSON): A list of commits, including their SHA.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the repository or branch does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    branch = request.args.get("branch")
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_branch_commits_page(
        owner, repo, branch, use_default, protocol, host, pat, end_cursor
    )
    return jsonify(data)


@github_bp.route(
    "/graphql/user_repository_names/<login>",
    methods=["GET"],
)
@jwt_required()
def user_repository_names(login):
    """
    Fetches the names of all repositories owned by a given GitHub user.

    URL Parameters:
        login (str): The GitHub username.

    Query Parameters:
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        Response (JSON): A list of repository names owned by the user.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the user does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_repository_names_page(login, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route(
    "/graphql/repository_contributor_contributions/<owner>/<repo>/<login>",
    methods=["GET"],
)
@jwt_required()
def repository_contributor_contributions(owner, repo, login):
    """
    Fetches commit contributions of a GitHub user in a specific repository.

    URL Parameters:
        owner (str): GitHub username of the repository owner.
        repo (str): Repository name.
        login (str): GitHub username of the contributor.

    Query Parameters:
        branch (str, optional): Branch name to filter commits.
        end_cursor (str, optional): Cursor for paginated results.

    Returns:
        Response (JSON): List of commits made by the contributor.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the repository or contributor does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    branch = request.args.get("branch")
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_contributor_contributions_page(
        owner, repo, branch, login, protocol, host, pat, end_cursor
    )
    return jsonify(data)


MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2


def fetch_with_retries(url, headers, max_retries=MAX_RETRIES, timeout=15):
    """
    Fetch data with retry logic and exponential backoff.

    Args:
        url (str): The URL to fetch data from.
        headers (dict): Headers for the request.
        max_retries (int, optional): Maximum number of retry attempts.
        timeout (int, optional): Request timeout in seconds.

    Returns:
        dict: JSON response if successful, or rate-limit response.

    Raises:
        Timeout: If all retry attempts are exhausted.
    """
    last_exception = None
    response = None

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code in {403, 429}:
                current_time = datetime.now(timezone.utc)
                reset_timestamp = int(response.headers.get("X-RateLimit-Reset"))
                reset_at = datetime.fromtimestamp(reset_timestamp, tz=timezone.utc)
                time_diff = reset_at - current_time
                seconds = time_diff.total_seconds()

                return {
                    "no_limit": True,
                    "wait_seconds": seconds + 3,
                    "reset_at": reset_at.isoformat(),
                }
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
            response.raise_for_status()

        except Timeout as e:
            last_exception = e
            logging.warning(
                "Request timed out. Retrying in %d seconds...",
                INITIAL_RETRY_DELAY * (2**attempt),
            )
            time.sleep(INITIAL_RETRY_DELAY * (2**attempt))

        except RequestException as e:
            last_exception = e
            logging.error("Request failed: %s. Retrying...", str(e))
            time.sleep(INITIAL_RETRY_DELAY * (2**attempt))
    raise Timeout("All retry attempts exhausted.") from last_exception


@github_bp.route("/rest/commits/<owner>/<repo>/<sha>", methods=["GET"])
@jwt_required()
def get_commit_details(owner, repo, sha):
    """
    Fetches details of a specific commit from GitHub.

    URL Parameters:
        owner (str): GitHub username of the repository owner.
        repo (str): Repository name.
        sha (str): SHA of the commit.

    Returns:
        Response (JSON): Commit details including author, stats, and language breakdown.

    Raises:
        401 Unauthorized: If the JWT token is invalid or missing.
        404 Not Found: If the commit does not exist.
        500 Internal Server Error: If an unexpected error occurs.
    """
    user = check_user()
    token, protocol, host = extract_user_credentials_and_host(user)
    headers = {"Authorization": f"token {token}"}

    # Fetch commit details with retry logic
    commit_url = f"{protocol}://{host}/repos/{owner}/{repo}/commits/{sha}"
    commit = fetch_with_retries(commit_url, headers)
    if isinstance(commit, dict) and commit.get("no_limit"):
        return jsonify(commit)

    if not commit:
        return (
            jsonify(
                {"error": "Failed to fetch commit details after multiple attempts"}
            ),
            500,
        )

    # Process commit details
    res = {
        "author": commit["commit"]["author"]["name"],
        "author_email": commit["commit"]["author"]["email"],
        "authoredDate": commit["commit"]["author"]["date"],
        "message": commit["commit"]["message"],
        "author_login": commit["author"]["login"] if commit["author"] else None,
        "parents": len(commit["parents"]),
        "additions": commit["stats"]["additions"],
        "deletions": commit["stats"]["deletions"],
        "changedFilesIfAvailable": len(commit["files"]),
        "lang_stats": {},
    }

    # Calculate language statistics
    for file in commit["files"]:
        try:
            lexer = guess_lexer_for_filename(file["filename"], file["patch"])
        except Exception:
            lexer = TextLexer()  # Default to plain text lexer if no lexer is found

        if lexer.name in res["lang_stats"]:
            res["lang_stats"][lexer.name]["additions"] += file["additions"]
            res["lang_stats"][lexer.name]["deletions"] += file["deletions"]
        else:
            res["lang_stats"][lexer.name] = {
                "additions": file["additions"],
                "deletions": file["deletions"],
            }

    return jsonify({"commit": res})
