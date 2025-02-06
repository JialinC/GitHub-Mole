"""This module set up necessary configuration for OAuth."""

from authlib.integrations.flask_client import OAuth
from app.config import AuthConfig

oauth = OAuth()


def config_oauth(app):
    """
    The config_oauth function initializes the OAuth client with the Flask app instance and
    registers GitHub as an OAuth provider using the app's configuration settings.
    It sets up the necessary URLs and scopes required for OAuth authentication with GitHub.
    """
    oauth.init_app(app)
    # Configure GitHub OAuth using environment variables
    oauth.register(
        name="github",
        client_id=AuthConfig.GITHUB_CLIENT_ID,
        client_secret=AuthConfig.GITHUB_CLIENT_SECRET,
        authorize_url=AuthConfig.GITHUB_AUTHORIZE_URL,
        access_token_url=AuthConfig.GITHUB_ACCESS_TOKEN_URL,
        client_kwargs={"scope": "user:email"},
    )
