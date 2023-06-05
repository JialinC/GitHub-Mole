from github_graphql.query import QueryNode, Query

import pandas as pd


class RepositoryGraph:
    STATS = [
        "totalRepositoryContributions",
        "totalCommitContributions",
        "totalIssueContributions",
        "totalPullRequestContributions",
        "totalPullRequestReviewContributions",
        "totalRepositoriesWithContributedCommits",
        "totalRepositoriesWithContributedIssues",
        "totalRepositoriesWithContributedPullRequests",
        "totalRepositoriesWithContributedPullRequestReviews",
    ]

    collaborations_collection_by_repository_query = QueryNode(
        name="commitContributionsByRepository",
        fields=[
            QueryNode(
                name="repository",
                fields=[
                    QueryNode(name="owner", fields=["login"]),
                    "name",
                    "url",
                ],
            ),
            QueryNode(
                name="contributions",
                args={"first": 100},
                fields=[
                    "totalCount",
                    QueryNode(name="pageInfo", fields=["endCursor", "hasNextPage"]),
                    QueryNode(
                        name="nodes",
                        fields=[
                            "commitCount",
                            "occurredAt",
                        ]
                    ),
                ]
            )
        ]
    )

    collaborations_collection_query = QueryNode(
        name="contributionsCollection",
        fields=[
            collaborations_collection_by_repository_query,
            "totalRepositoryContributions",
            "totalCommitContributions",
            "totalIssueContributions",
            "totalPullRequestContributions",
            "totalPullRequestReviewContributions",
            "totalRepositoriesWithContributedCommits",
            "totalRepositoriesWithContributedIssues",
            "totalRepositoriesWithContributedPullRequests",
            "totalRepositoriesWithContributedPullRequestReviews",
        ]
    )

    collaborators_query = QueryNode(
        name="collaborators",
        args={"first": 100},
        fields=[
            "totalCount",
            QueryNode(name="pageInfo", fields=["endCursor", "hasNextPage"]),
            QueryNode(
                name="nodes",
                fields=[
                    "login",
                    "name",
                    collaborations_collection_query
                ]
            ),
        ]
    )

    repository_query = QueryNode(
        name="repository",
        args={"name": "$repository"},
        fields=[
            "name",
            "createdAt",
            "updatedAt",
            "forkCount",
            "stargazerCount",
            QueryNode(name="watchers", fields=["totalCount"]),
            QueryNode(name="primaryLanguage", fields=["name"]),
            collaborators_query,
            QueryNode(
                name="languages",
                args={"first": 100},
                fields=[
                    "totalCount",
                    QueryNode(name="pageInfo", fields=["endCursor", "hasNextPage"]),
                    QueryNode(name="nodes", fields=["name"]),
                ]
            )
        ]
    )

    query = Query(
        fields=[
            QueryNode(
                name="user",
                args={"login": "$user"},
                fields=[
                    "login",
                    repository_query,
                ]
            )
        ]
    )

    @staticmethod
    def collect_collaborator_stats(data: dict, stat: str):
        return dict(
            pd.Series([_collaborator["contributionsCollection"][stat] for _collaborator in data]).describe()
        )

    @staticmethod
    def collect_collaborator_repository_stats(data: dict, owner: str, repository: str):
        return {
            _collaborator["login"]:
            next(
                _repo["contributions"]["totalCount"]
                for _repo in _collaborator["contributionsCollection"]["commitContributionsByRepository"]
                if _repo["repository"]["name"] == repository and _repo["repository"]["owner"]["login"] == owner
            )
            for _collaborator in data
        }

    @staticmethod
    def flatten_result(raw: dict):
        flat_data = {
            "owner": raw["user"]["login"],
            "repository_name": raw["user"]["repository"]["name"],
            "repository_created_at": raw["user"]["repository"]["createdAt"],
            "repository_updated_at": raw["user"]["repository"]["updatedAt"],
            "repository_languages": [
                _language["name"] for _language in raw["user"]["repository"]["languages"]["nodes"]
            ],
            "repository_primary_language": raw["user"]["repository"]["primaryLanguage"]["name"],
            "repository_collaborator_count": raw["user"]["repository"]["collaborators"]["totalCount"],
            "repository_watchers_count":  raw["user"]["repository"]["watchers"]["totalCount"],
            "repository_fork_count": raw["user"]["repository"]["forkCount"],
            "repository_stargazer_count": raw["user"]["repository"]["stargazerCount"],
            "repository_collaborator_commit_stats_total": RepositoryGraph.collect_collaborator_repository_stats(
                raw["user"]["repository"]["collaborators"]["nodes"],
                owner=raw["user"]["login"],
                repository=raw["user"]["repository"]["name"]
            )
        }

        for stat in RepositoryGraph.STATS:
            flat_data[f"repository_collaborator_{stat}_stats"] = RepositoryGraph.collect_collaborator_stats(
                data=raw["user"]["repository"]["collaborators"]["nodes"],
                stat=stat,
            )

        return flat_data
