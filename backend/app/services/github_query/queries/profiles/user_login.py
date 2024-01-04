from backend.app.services.github_query.github_graphql.query import QueryNode, Query

class UserLoginViewer(Query):
    """
    UserLoginViewer is a subclass of Query designed to fetch the viewer's login information using the 'viewer' field in a GraphQL query.
    """
    
    def __init__(self) -> None:
        """
        Initializes a UserLoginViewer object to fetch the current authenticated user's login name.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "viewer",
                    fields=["login"]  # 'login' is typically the username in GitHub.
                )
            ]
        )


class UserLogin(Query):
    """
    UserLogin is a subclass of Query designed to fetch a specific user's login and other profile information using the 'user' field in a GraphQL query.
    """
    
    def __init__(self) -> None:
        """
        Initializes a UserLogin object to fetch specified user information including login, name, id, email, and creation date.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={
                        "login": "$user"  # Variable to be substituted with actual user login.
                    },
                    fields=[
                        "login",    # The username or login name of the user.
                        "name",     # The full name of the user.
                        "id",       # The unique ID of the user.
                        "email",    # The email address of the user.
                        "createdAt" # The creation date of the user's account.
                    ]
                )
            ]
        )
