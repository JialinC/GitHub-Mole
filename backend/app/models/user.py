"""The module defines the User class, which users can utilize to mine GitHub users' contribution metrics."""

from app.database import db


class User(db.Model):
    """
    The User class is a data model that represents users within the application,
    designed to work with a SQLAlchemy ORM as part of a Flask application.
    This class provides a structure for storing user information,
    including their username, email, and a token for GitHub authentication.
    Additionally, it establishes a relationship with the GitHubUserData model,
    allowing for the association of GitHub-specific metrics with each user.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    github_token = db.Column(db.String(255), nullable=False)
    github_data = db.relationship("GitHubUserData", backref="user", lazy="dynamic")
