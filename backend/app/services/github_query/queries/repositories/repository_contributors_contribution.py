from typing import Dict, List, Optional, Any
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator

class RepositoryContributorsContribution(PaginatedQuery):
    def __init__(self) -> None:
        """
        Initializes a paginated query to extract contributions made by contributors in a specific repository.
        Focuses on the commit history of the repository's default branch, targeting individual contributions.
        """
        super().__init__(
            fields=[
                QueryNode(
                    "repository",
                    args={"owner": "$owner", "name": "$repo_name"},
                    fields=[
                        QueryNode(
                            "defaultBranchRef",
                            fields=[
                                QueryNode(
                                    "target",
                                    fields=[
                                        QueryNode(
                                            "... on Commit",
                                            fields=[
                                                QueryNodePaginator(
                                                    "history",
                                                    args={"author": "$id", "first": "$pg_size"},
                                                    fields=[
                                                        "totalCount",
                                                        QueryNode(
                                                            "nodes",
                                                            fields=[
                                                                "authoredDate",
                                                                "changedFilesIfAvailable",
                                                                "additions",
                                                                "deletions",
                                                                "message",
                                                                QueryNode(
                                                                    "parents (first: 2)",
                                                                    fields=["totalCount"]
                                                                )
                                                            ]
                                                        ),
                                                        QueryNode(
                                                            "pageInfo",
                                                            fields=["endCursor", "hasNextPage"]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    @staticmethod
    def user_cumulated_contribution(raw_data: Dict[str, Any], cumulative_contribution: Optional[Dict[str, int]] = None) -> Dict[str, int]:
        """
        Calculates cumulative contribution statistics of a user from the provided raw data.

        Args:
            raw_data (Dict): Raw data returned by the GraphQL query.
            cumulative_contribution (Optional[Dict[str, int]]): A dictionary to accumulate contributions. 
                                                               If None, a new dictionary is initialized.

        Returns:
            Dict[str, int]: A dictionary containing the cumulative statistics: total additions, deletions, and commits.
        """
        nodes = raw_data['repository']['defaultBranchRef']['target']['history']['nodes']
        if cumulative_contribution is None:
            cumulative_contribution = {'total_additions': 0, 'total_deletions': 0, 'total_commits': 0}
        
        for node in nodes:
            if node['parents'] and node['parents']['totalCount'] < 2:
                cumulative_contribution['total_additions'] += node['additions']
                cumulative_contribution['total_deletions'] += node['deletions']
                cumulative_contribution['total_commits'] += 1
        
        return cumulative_contribution

    @staticmethod
    def user_commit_contribution(raw_data: Dict[str, Any], commit_contributions: Optional[List[Dict[str, int]]] = None) -> List[Dict[str, int]]:
        """
        Extracts and compiles individual commit contributions from the raw data.

        Args:
            raw_data (Dict): Raw data returned by the GraphQL query.
            commit_contributions (Optional[List[Dict[str, int]]]): A list to accumulate individual commit contributions.

        Returns:
            List[Dict[str, int]]: A list of dictionaries, each representing details of an individual commit.
        """
        nodes = raw_data['repository']['defaultBranchRef']['target']['history']['nodes']
        if commit_contributions is None:
            commit_contributions = []
        
        for node in nodes:
            if node['parents'] and node['parents']['totalCount'] < 2:
                commit_contributions.append({
                    'authoredDate': node['authoredDate'],
                    'changedFiles': node['changedFilesIfAvailable'],
                    'additions': node['additions'],
                    'deletions': node['deletions'],
                    'message': node['message']
                })
        
        return commit_contributions
