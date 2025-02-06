import pytest
from backend.app.services.github_query.github_graphql.authentication import Authenticator, PersonalAccessTokenAuthenticator 

def test_authenticator_raises():
    """
    Test that the base Authenticator class raises NotImplementedError
    when trying to call get_authorization_header without a subclass implementation.
    """
    authenticator = Authenticator()
    with pytest.raises(NotImplementedError):
        authenticator.get_authorization_header()

def test_personal_access_token_authenticator():
    """
    Test the PersonalAccessTokenAuthenticator for correct header format and initialization.
    """
    token = "test_token_123"
    authenticator = PersonalAccessTokenAuthenticator(token=token)

    # Test initialization
    assert authenticator._token == token, "Token should be set correctly in the authenticator."

    # Test get_authorization_header method
    expected_header = {"Authorization": f"token {token}"}
    assert authenticator.get_authorization_header() == expected_header, "The authorization header should be formatted correctly."

