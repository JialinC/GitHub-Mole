from backend.app.services.github_query.github_graphql.query import QueryNode, Query

class UserLoginViewer(Query):
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
                        "id",
                        "email",
                        "createdAt"
                    ]
                )
            ]
        )
