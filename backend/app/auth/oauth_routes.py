"""The module defines necessary endpoints for GitHub OAuth"""

from flask import Blueprint, redirect, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.config import AuthConfig
from app.config import Config
from .oauth import oauth  # Import the OAuth object configured for GitHub integration.


# Create a Blueprint for authentication-related routes. This organizes auth routes under a common namespace.
auth_bp = Blueprint("oauth", __name__)


@auth_bp.route("/authorize")
def authorize():
    """
    Route: /authorize
    Method: GET
    Description: Initiates the OAuth login process with GitHub. It constructs the OAuth authorization URL
    and redirects the user to GitHub's authorization page to grant or deny access.
    Returns: A redirection response leading the user to GitHub's OAuth authorization page.
    Usage: No parameters are required. Access this endpoint to start the login process through GitHub OAuth.
    """
    # Dynamically generate the callback URL to be used after GitHub authorization.
    redirect_uri = url_for("oauth.callback", _external=True)

    # Redirect the user to GitHub's authorization page, passing along the callback URL.
    return oauth.github.authorize_redirect(redirect_uri)


@auth_bp.route("/callback")
def callback():
    """
    Route: /callback
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

    # Store the access token and user info in the session or database
    github_login = user_info["login"]
    github_id = str(user_info["node_id"])
    personal_access_token = token["access_token"]
    api_url = AuthConfig.GITHUB_API_BASE_URL
    user = User.query.filter_by(github_login=github_login).first()
    if user:
        user.update(personal_access_token=personal_access_token)
    else:
        User.create(
            github_id=github_id,
            github_login=github_login,
            personal_access_token=personal_access_token,
            api_url=api_url,
        )

    # Generate JWT token
    access_token = create_access_token(identity=github_id)
    refresh_token = create_refresh_token(identity=github_id)

    # Redirect to the frontend with the token included in the URL
    return redirect(
        f"{Config.FRONTEND_URL}/dashboard?access_token={access_token}&refresh_token={refresh_token}"
    )


@auth_bp.route("/logout")
def logout():
    """
    Route: /logout
    Method: GET
    Description: Logs the user out of the application by clearing all session data and redirects them to the index page.
    Returns: A redirection response to the index page.
    Usage: Access this endpoint to log out from the application, clearing any session-stored user data.
    """
    # Redirect the user back to the index page.
    return redirect(url_for("index"))
