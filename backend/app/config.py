"""This module provides a foundational setup for configuring a web application, specifically designed to interact with
GitHub's GraphQL API and a MySQL database. The configurations are divided into different classes, each serving a
specific purpose, making the application modular, easy to manage, and scalable."""

# import os


class Config:
    """The base configuration class that sets up essential configurations applicable across the application."""

    DEBUG = True  # Ensure debug is enabled in your configuration for development
    SECRET_KEY = "your_secret_key_here"  # Consider using environment variables


class AuthConfig(Config):
    """This class extends Config and includes configurations specific to GitHub OAuth authentication."""

    GITHUB_OAUTH_CLIENT_ID = "918ef50cd94282d71b1b"
    GITHUB_OAUTH_CLIENT_SECRET = "9d8242fe2293c6d8784f48ee6ba6117d1cb4e748"


class DBConfig(Config):
    """This class, also extending Config, contains configurations necessary for connecting to and
    interacting with a MySQL database."""

    MYSQL_DATABASE_USER = "tester"
    MYSQL_DATABASE_PASSWORD = "password"
    MYSQL_DATABASE_DB = "github_graphql"
    MYSQL_DATABASE_HOST = "localhost"  # or your MySQL server address
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_DATABASE_USER}:"
        f"{MYSQL_DATABASE_PASSWORD}@{MYSQL_DATABASE_HOST}/"
        f"{MYSQL_DATABASE_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
