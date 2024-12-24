"""This file defines the URLs for various GraphQL endpoints."""

from urllib.parse import urlparse
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.database import db
from backend.app.models.user import User
import logging

# Import service methods
# from ..services.github_repository_services import (
#     get_repository_contributors,
#     get_contributor_contributions,
#     get_repository_commits,
# )
from ..services.github_graphql_services import (
    get_current_user_login,
    get_specific_user_login,
    get_user_commit_comments_page,
)

github_bp = Blueprint("api", __name__)


def check_user():
    github_id = get_jwt_identity()
    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        logging.error("User with GitHub ID %s not found", github_id)
        return jsonify({"msg": "User not found"}), 404
    return user


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
    pat = user.personal_access_token
    parsed_url = urlparse(user.api_url)
    protocol = parsed_url.scheme
    host = parsed_url.netloc
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
    pat = user.personal_access_token
    parsed_url = urlparse(user.api_url)
    protocol = parsed_url.scheme
    host = parsed_url.netloc
    data = get_specific_user_login(login, protocol, host, pat)
    return jsonify(data)


@github_bp.route("/graphql/user-commit-comments/<login>", methods=["GET"])
@jwt_required()
def user_commit_comments(login):
    """
    Route:
    Method: GET
    """
    end_cursor = request.args.get("end_cursor")
    # hasNextPage = request.args.get("hasNextPage")
    print("end_cursor:", end_cursor)
    # print("hasNextPage:", hasNextPage)
    user = check_user()
    pat = user.personal_access_token
    parsed_url = urlparse(user.api_url)
    protocol = parsed_url.scheme
    host = parsed_url.netloc
    data = get_user_commit_comments_page(login, protocol, host, pat, end_cursor)
    # print("route response:", data)
    return jsonify(data)
