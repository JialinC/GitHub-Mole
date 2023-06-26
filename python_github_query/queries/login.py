from github_graphql.query import Query, QueryNode


class UserLoginViewer(Query):
    """
    The raw GraphQL query:
    query {
        viewer {
            login
        }
    }
    """
    query = Query(
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
    query = Query(
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
