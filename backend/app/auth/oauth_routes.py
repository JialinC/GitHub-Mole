"""The module defines necessary endpoints for GitHub OAuth"""

from flask import Blueprint, redirect, url_for, session
from .oauth import oauth  # Import the OAuth object configured for GitHub integration.

# Create a Blueprint for authentication-related routes. This organizes auth routes under a common namespace.
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    """
    Route: /login
    Method: GET
    Description: Initiates the OAuth login process with GitHub. It constructs the OAuth authorization URL
    and redirects the user to GitHub's authorization page to grant or deny access.
    Returns: A redirection response leading the user to GitHub's OAuth authorization page.
    Usage: No parameters are required. Access this endpoint to start the login process through GitHub OAuth.
    """
    # Dynamically generate the callback URL to be used after GitHub authorization.
    redirect_uri = url_for("auth.authorize", _external=True)

    # Redirect the user to GitHub's authorization page, passing along the callback URL.
    return oauth.github.authorize_redirect(redirect_uri)


@auth_bp.route("/login/authorize")
def authorize():
    """
    Route: /login/authorize
    Method: GET
    Description: Serves as the OAuth callback to handle the response from GitHub post-user authorization.
    It exchanges the authorization code for an access token, fetches the user's GitHub profile, and stores essential
    information in the session.
    Returns: A redirection response to the application's index page after successful authorization.
    Usage: This endpoint is primarily used as a callback URL during the OAuth process and
    isn't typically accessed directly by users.
    """
    # Exchange the authorization code for an access token.
    token = oauth.github.authorize_access_token()

    # Use the access token to fetch the user's GitHub profile information.
    resp = oauth.github.get("user", token=token)
    user_info = resp.json()  # Convert the response to JSON to extract user details.

    # Store the access token and GitHub login in the session for future use.
    session["access_token"] = token["access_token"]
    session["login"] = user_info["login"]

    # Redirect the user to the application's index page after successful authorization.
    return redirect(url_for("index"))


@auth_bp.route("/logout")
def logout():
    """
    Route: /logout
    Method: GET
    Description: Logs the user out of the application by clearing all session data and redirects them to the index page.
    Returns: A redirection response to the index page.
    Usage: Access this endpoint to log out from the application, clearing any session-stored user data.
    """
    # Clear all data from the session to log the user out.
    session.clear()

    # Redirect the user back to the index page.
    return redirect(url_for("index"))
