"""This module provides a foundational setup for configuring a web application, specifically designed to interact with
GitHub's GraphQL API and a MySQL database. The configurations are divided into different classes, each serving a
specific purpose, making the application modular, easy to manage, and scalable."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """The base configuration class that sets up essential configurations applicable across the application."""

    DEBUG = True
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    # SESSION_COOKIE_HTTPONLY = True
    # SESSION_COOKIE_SAMESITE = "Lax"
    # SESSION_COOKIE_SECURE = False
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


class AuthConfig(Config):
    """This class extends Config and includes configurations specific to GitHub OAuth authentication."""

    GITHUB_CLIENT_ID = os.getenv("GITHUB_OAUTH_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_OAUTH_CLIENT_SECRET")
    GITHUB_AUTHORIZE_URL = f"{os.getenv('GITHUB_HOSTNAME')}/login/oauth/authorize"
    GITHUB_ACCESS_TOKEN_URL = f"{os.getenv('GITHUB_HOSTNAME')}/login/oauth/access_token"
    GITHUB_API_BASE_URL = os.getenv("GITHUB_API_URL")


class DBConfig(Config):
    """This class, also extending Config, contains configurations necessary for connecting to and
    interacting with a MySQL database."""

    MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER")
    MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD")
    MYSQL_DATABASE_DB = os.getenv("MYSQL_DATABASE_DB")
    MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_DATABASE_USER}:"
        f"{MYSQL_DATABASE_PASSWORD}@{MYSQL_DATABASE_HOST}/"
        f"{MYSQL_DATABASE_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
