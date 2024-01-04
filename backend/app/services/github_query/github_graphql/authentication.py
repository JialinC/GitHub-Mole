from typing import Dict

class Authenticator:
    """
    Authenticator is an abstract base class for handling different types of 
    authentication methods for GitHub clients. It provides a common interface 
    for authentication by defining a method to get the authorization header.
    """
    def get_authorization_header(self) -> Dict[str, str]:
        """
        Abstract method to get the authorization header. Implementations of this 
        method in subclasses should return the necessary header for authentication 
        based on the specific method they represent.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Authenticator cannot be implemented")


class PersonalAccessTokenAuthenticator(Authenticator):
    """
    PersonalAccessTokenAuthenticator is a concrete implementation of the Authenticator class,
    providing authentication functionality specifically using a personal access token for GitHub.
    """
    def __init__(self, token: str):
        """
        Initializes the authenticator with a personal access token.

        Args:
            token (str): The personal access token used for authentication.
        """
        self._token = token

    def get_authorization_header(self) -> Dict[str, str]:
        """
        Constructs and returns the authorization header using the personal access token.

        Returns:
            dict: A dictionary representing the authorization header required for 
                  authentication with the GitHub API using a personal access token.
        """
        return {
            "Authorization": f"token {self._token}"
        }
