class Authenticator:
    """
    Handles Authentication Method for GitHub clients.
    """
    def get_authorization_header(self):
        raise NotImplementedError("Authenticator cannot be implemented")


class PersonalAccessTokenAuthenticator(Authenticator):
    """
    Handles Personal Access Token Authentication Method for GitHub clients
    """
    def __init__(self, token: str):
        """
        Sets the Authentication Personal Access Token.
        Args:
            token: Personal Access Token
        """
        self._token = token

    def get_authorization_header(self):
        """
        Returns the authentication header.
        Returns:
            Authentication Header
        """
        return {
            "Authorization": f"token {self._token}"
        }
