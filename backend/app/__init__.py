from flask import Flask
from .auth.config import Config
from .auth.oauth import config_oauth
from .auth.oauth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations
    app.debug = app.config.get('DEBUG', False)

    config_oauth(app)  # Initialize OAuth with app configuration

    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register the Blueprint

    return app