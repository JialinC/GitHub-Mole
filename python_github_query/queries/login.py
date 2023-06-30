from python_github_query.github_graphql.query import Query, QueryNode


class UserLoginViewer(Query):
    """
    The raw GraphQL query:
    query {
        viewer {
            login
        }
    }
    """
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "viewer",
                    fields=["login"]
                )
            ]
        )


class UserLogin(Query):
    """
    The raw GraphQL query
    query ($user: String!){
        user(login: $user){
            login
            name
            email
            createdAt
        }
    }
    """
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={
                        "login": "$user"
                    },
                    fields=[
                        "login",
                        "name",
                        "email",
                        "createdAt"
                    ]
                )
            ]
        )
