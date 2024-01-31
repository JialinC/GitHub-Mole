from flask import Flask
from flask_migrate import Migrate
from .database import db
from .config import Config, AuthConfig, DBConfig
from .auth.oauth import config_oauth
from .auth.oauth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    # Load configurations
    app.config.from_object(Config)
    app.config.from_object(AuthConfig)
    app.config.from_object(DBConfig)
    app.debug = app.config.get('DEBUG', False)

    config_oauth(app)  # Initialize OAuth with app configuration

    db.init_app(app)
    migrate = Migrate(app, db)

    # Import models to ensure they are registered with SQLAlchemy
    from .models import user, github_user_data

    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register the Blueprint

    return app