"""This file defines the URLs for various GraphQL endpoints."""

from flask import Blueprint, jsonify

# Import service methods
from backend.app.services.github_graphql_services import (
    get_current_user_login,
    get_specific_user_login,
)

github_bp = Blueprint("api", __name__)


@github_bp.route("/graphql/current-user-login", methods=["GET"])
def current_user_login():
    """
    Route: /graphql/current-user-login
    Method: GET
    Description: Fetches the login details of the current authenticated user.
    Returns: A JSON object containing the login information of the current user.
    """
    data = get_current_user_login()
    return jsonify(data)


@github_bp.route("/graphql/user-login/<username>", methods=["GET"])
def specific_user_login(username):
    """
    Route: /graphql/user-login/<username>
    Method: GET
    URL Parameter: username - The GitHub username of the user for whom to fetch login details.
    Description: Retrieves the login details for a specific GitHub user identified by their username.
    Returns: A JSON object containing the login information of the specified user.
    """
    data = get_specific_user_login(username)
    return jsonify(data)
