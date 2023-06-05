from github_graphql.query import Query, QueryNode


class UserLoginViewer(Query):
    query = QueryNode(
        fields=[
            QueryNode(
                "viewer",
                fields=["login"]
            )
        ]
    )


class UserLogin(Query):
    query = QueryNode(
        fields=[
            QueryNode(
                "user",
                args={
                    "login": "$user"
                },
                fields=[
                    "login", "name", "email", "createdAt"
                ]
            )
        ]
    )
