from github_query.github_graphql.query import Query, QueryNode


class RateLimit(Query):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "rateLimit",
                    args={
                        "dryRun": "$dryrun"
                    },
                    fields=[
                        "cost",
                        "limit",
                        "remaining",
                        "resetAt",
                        "used"
                    ]
                )
            ]
        )
