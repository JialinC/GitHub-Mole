from github_query.github_graphql.query import Query, QueryNode


class QueryCost(Query):
    def __init__(self, test):
        super().__init__(
            fields=[
                test,
                QueryNode(
                    "rateLimit",
                    args={
                        "dryRun": "$dryrun"
                    },
                    fields=[
                        "cost",
                        "remaining",
                        "resetAt"
                    ]
                )
            ]
        )
