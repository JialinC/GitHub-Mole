from flask import session
from typing import Union, Optional, Dict, Any, Generator
# Import client, exceptions, and authentication classes
from backend.app.services.github_query.github_graphql.client import Client, QueryFailedException
from backend.app.services.github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
# Import query classes
from backend.app.services.github_query.queries.profiles.user_login import UserLoginViewer, UserLogin

def get_current_user_login():
    """
    Fetches the login information of the current authenticated user using the OAuth access token.
    
    Returns:
        dict: A dictionary containing the current user's login information, or an error message.
    """
    # Retrieve the OAuth access token from the session
    token = session.get('access_token')
    if not token:
        return {"error": "User not authenticated"}
    
    client = Client(host="api.github.com", is_enterprise=False, authenticator=PersonalAccessTokenAuthenticator(token=token))

    try:
        query = UserLoginViewer()
        response = client.execute(query=query, substitutions={})
        return response
    except QueryFailedException as e:
        return {"error": str(e)}

def get_specific_user_login(username: str):
    """
    Fetches the login and profile information of a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the specified user's login and profile information.
    """
    # Retrieve the OAuth access token from the session
    token = session.get('access_token')
    if not token:
        return {"error": "User not authenticated"}
    client = Client(host="api.github.com", is_enterprise=False, authenticator=PersonalAccessTokenAuthenticator(token=token))

    try:
        query = UserLogin()
        response = client.execute(query, substitutions={"user": username})
        return response
    except QueryFailedException as e:
        return {"error": str(e)}