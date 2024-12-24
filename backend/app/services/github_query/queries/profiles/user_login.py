"""The module defines several classes that formulate GraphQL query string to extract basic user profile information."""

from ..query import QueryNode, Query
from ..constants import (
    NODE_VIEWER,
    NODE_USER,
    FIELD_LOGIN,
    FIELD_NAME,
    FIELD_ID,
    FIELD_EMAIL,
    FIELD_CREATED_AT,
    ARG_LOGIN,
)


class UserLoginViewer(Query):
    """
    UserLoginViewer is a subclass of Query designed to fetch the viewer's login information using the 'viewer' field
    in a GraphQL query.
    """

    def __init__(self) -> None:
        """
        Initializes a UserLoginViewer object to fetch the current authenticated user's login name.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_VIEWER,
                    fields=[FIELD_LOGIN],
                )
            ]
        )


class UserLogin(Query):
    """
    UserLogin is a subclass of Query designed to fetch a specific user's login and
    other profile information using the 'user' field in a GraphQL query.
    """

    def __init__(self, login: str) -> None:
        """
        Initializes a UserLogin object to fetch specified user information including login, name, id, email,
        and creation date.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={
                        ARG_LOGIN: login  # Variable to be substituted with actual user login.
                    },
                    fields=[
                        FIELD_LOGIN,  # The username or login name of the user.
                        FIELD_NAME,  # The full name of the user.
                        FIELD_ID,  # The unique ID of the user.
                        FIELD_EMAIL,  # The email address of the user.
                        FIELD_CREATED_AT,  # The creation date of the user's account.
                    ],
                )
            ]
        )
