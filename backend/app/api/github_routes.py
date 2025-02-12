"""This file defines the URLs for various GraphQL endpoints."""

from urllib.parse import urlparse
from datetime import datetime, timezone
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.special import TextLexer
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
import logging
import requests

# Import service methods
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
    get_repository_contributors_page,
    get_repository_branch_commits_page,
    get_repository_contributor_contributions_page,
    get_user_repository_names_page,
)

github_bp = Blueprint("api", __name__)


def check_user():
    github_id = get_jwt_identity()
    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        logging.error("User with GitHub ID %s not found", github_id)
        return jsonify({"msg": "User not found"}), 404
    return user


def extract_user_credentials_and_host(user):
    pat = user.personal_access_token
    parsed_url = urlparse(user.api_url)
    protocol = parsed_url.scheme
    host = parsed_url.netloc
    return pat, protocol, host


@github_bp.route("/graphql/rate-limit", methods=["GET"])
@jwt_required()
def rate_limit():
    """
    Route: /graphql/current-user-login
    Method: GET
    Description: Fetches the login details of the current authenticated user.
    Returns: A JSON object containing the login information of the current user.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_rate_limit(protocol=protocol, host=host, token=pat)
    return jsonify(data)


@github_bp.route("/graphql/current-user-login", methods=["GET"])
@jwt_required()
def current_user_login():
    """
    Route: /graphql/current-user-login
    Method: GET
    Description: Fetches the login details of the current authenticated user.
    Returns: A JSON object containing the login information of the current user.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_current_user_login(protocol=protocol, host=host, token=pat)
    return jsonify(data)


@github_bp.route("/graphql/user-login/<login>", methods=["GET"])
@jwt_required()
def specific_user_login(login):
    """
    Route: /graphql/user-login/<username>
    Method: GET
    URL Parameter: username - The GitHub username of the user for whom to fetch login details.
    Description: Retrieves the login details for a specific GitHub user identified by their username.
    Returns: A JSON object containing the login information of the specified user.
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_specific_user_login(login, protocol, host, pat)
    return jsonify(data)


@github_bp.route("/graphql/user-profile-stats/<login>", methods=["GET"])
@jwt_required()
def user_profile_stats(login):
    """
    Route:
    Method:
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
    Route:
    Method:
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
    Route:
    Method:
    """
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_user_contribution_years(login, protocol, host, pat)
    return jsonify(data)


@github_bp.route("/graphql/user-contribution-calendar/<login>", methods=["GET"])
@jwt_required()
def user_contribution_calendar(login):
    """
    Route:
    Method:
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
    Route:
    Method:
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
    Route:
    Method:
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
    Route:
    Method:
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
    Route:
    Method:
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
    Route:
    Method: GET
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
    Route:
    Method: GET
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
    Route:
    Method: GET
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
    Route:
    Method: GET
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
    Route:
    Method: GET
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
    Route:
    Method: GET
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
    Route:
    Method: GET
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
    Route:
    Method: GET
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
    Route:
    Method: GET
    """
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_branches_page(owner, repo, protocol, host, pat, end_cursor)
    return jsonify(data)


@github_bp.route("/graphql/repository_contributors/<owner>/<repo>", methods=["GET"])
@jwt_required()
def repository_contributors(owner, repo):
    """
    Route:
    Method: GET
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
    Route:
    Method: GET
    """
    branch = request.args.get("branch")
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_branch_commits_page(
        owner, repo, branch, use_default, protocol, host, pat, end_cursor
    )
    return jsonify(data)


# mining all commits details
@github_bp.route(
    "/graphql/user_repository_names/<login>",
    methods=["GET"],
)
@jwt_required()
def user_repository_names(login):
    """
    Route:
    Method: GET
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
    Route:
    Method: GET
    """
    branch = request.args.get("branch")
    end_cursor = request.args.get("end_cursor")
    user = check_user()
    pat, protocol, host = extract_user_credentials_and_host(user)
    data = get_repository_contributor_contributions_page(
        owner, repo, branch, login, protocol, host, pat, end_cursor
    )
    return jsonify(data)


@github_bp.route(
    "/rest/commits/<owner>/<repo>/<sha>",
    methods=["GET"],
)
@jwt_required()
def get_commit_details(owner, repo, sha):
    """
    Route:
    Method: GET
    """
    user = check_user()
    token, protocol, host = extract_user_credentials_and_host(user)
    rate_limit_url = f"{protocol}://{host}/rate_limit"
    headers = {"Authorization": f"token {token}"}
    try:
        response = requests.get(rate_limit_url, headers=headers, timeout=10)
        response.raise_for_status()
        rate_limit_data = response.json()
        remaining_requests = rate_limit_data["rate"]["remaining"]
        reset_time = rate_limit_data["rate"]["reset"]
        reset_at = datetime.fromtimestamp(reset_time, tz=timezone.utc)
        current_time = datetime.now(timezone.utc)
        time_diff = reset_at - current_time
        seconds = time_diff.total_seconds()
        if remaining_requests == 0:
            return (
                jsonify(
                    {
                        "no_limit": True,
                        "error": "Rate limit exceeded",
                        "wait_seconds": seconds + 2,
                        "reset_at": reset_at.isoformat(),
                        "message": "Try again after the reset time.",
                    }
                ),
                200,
            )

        commit_url = f"{protocol}://{host}/repos/{owner}/{repo}/commits/{sha}"
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.get(commit_url, headers=headers, timeout=10)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    logging.warning(
                        "Attempt %d failed: %s. Retrying...", attempt + 1, str(e)
                    )
                    continue
                else:
                    logging.error("All retry attempts failed: %s", str(e))
                    return (
                        jsonify(
                            {
                                "error": "Failed to fetch commit details after multiple attempts"
                            }
                        ),
                        500,
                    )
        commit = response.json()
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
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
