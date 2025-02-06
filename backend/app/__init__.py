from flask import Flask
from flask_migrate import Migrate
from .database import db
from .config import Config, AuthConfig, DBConfig
from .auth.oauth import config_oauth
from .auth.oauth_routes import auth_bp
from .api.github_routes import github_bp
from .api.helper_routes import helper_bp
from .api.team_routes import team_bp
from .api.db_routes import db_bp
import logging


def create_app():
    app = Flask(__name__)
    # Load configurations
    app.config.from_object(Config)
    app.config.from_object(AuthConfig)
    app.config.from_object(DBConfig)
    app.debug = app.config.get("DEBUG", False)

    config_oauth(app)  # Initialize OAuth with app configuration

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    if app.config["GITHUB_CLIENT_ID"]:
        app.register_blueprint(auth_bp, url_prefix="/oauth")
        print(app.config["GITHUB_CLIENT_ID"])
    else:
        print("GITHUB_CLIENT_ID not set")
    app.register_blueprint(github_bp, url_prefix="/api")
    app.register_blueprint(helper_bp, url_prefix="/api")
    app.register_blueprint(team_bp, url_prefix="/api")
    app.register_blueprint(db_bp, url_prefix="/api")

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    return app
