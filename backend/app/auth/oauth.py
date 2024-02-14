from flask import url_for
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def config_oauth(app):
    oauth.init_app(app)

    def get_redirect_uri():
        # Use url_for inside a function to ensure it's called within a request context
        return url_for('auth.authorize', _external=True, _scheme='https')

    oauth.register(
        name='github',
        client_id=app.config['GITHUB_OAUTH_CLIENT_ID'],
        client_secret=app.config['GITHUB_OAUTH_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}, # extend this to meet project requirements
        # Pass the function get_redirect_uri as the redirect_uri argument
        redirect_uri=get_redirect_uri
    )