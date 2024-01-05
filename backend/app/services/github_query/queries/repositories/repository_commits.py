from typing import Dict, List, Optional
from backend.app.services.github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator

class RepositoryCommits(PaginatedQuery):
    def __init__(self) -> None:
        """Initializes a paginated query for repository commits with specific fields and pagination controls."""
        super().__init__(
            fields=[
                QueryNode(
                    "repository",
                    args={"owner": "$owner", "name": "$repo_name"},  # Query arguments for specifying the repository
                    fields=[
                        QueryNode(
                            "defaultBranchRef",  # Points to the default branch of the repository
                            fields=[
                                QueryNode(
                                    "target",
                                    fields=[
                                        QueryNode(
                                            "... on Commit",  # Inline fragment on Commit type
                                            fields=[
                                                QueryNodePaginator(
                                                    "history",  # Paginated history of commits
                                                    args={"first": "$pg_size"},  # Pagination control arguments
                                                    fields=[
                                                        'totalCount',  # Total number of commits in the history
                                                        QueryNode(
                                                            "nodes",  # List of commit nodes
                                                            fields=[
                                                                "authoredDate",  # Date when the commit was authored
                                                                "changedFilesIfAvailable",  # Number of files changed, if available
                                                                "additions",  # Number of additions made in the commit
                                                                "deletions",  # Number of deletions made in the commit
                                                                "message",  # Commit message
                                                                QueryNode(
                                                                    "parents (first: 2)",  # Parent commits of the commit, limited to 2
                                                                    fields=[
                                                                        "totalCount"  # Total number of parent commits
                                                                    ]
                                                                ),
                                                                QueryNode(
                                                                    "author",  # Author of the commit
                                                                    fields=[
                                                                        'name',  # Name of the author
                                                                        'email',  # Email of the author
                                                                        QueryNode(
                                                                            "user",  # User associated with the author
                                                                            fields=[
                                                                                "login"  # Login of the user
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        QueryNode(
                                                            "pageInfo",  # Information about pagination
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
    def commits_list(raw_data: Dict[str, Dict], cumulative_commits: Optional[Dict[str, Dict]] = None) -> Dict[str, Dict]:
        """
        Processes the raw data from the GraphQL query to accumulate commit data per author.

        Args:
            raw_data: The raw data returned from the GraphQL query.
            cumulative_commits: Optional cumulative commits dictionary to accumulate results.

        Returns:
            A dictionary of cumulative commit data per author, with details like total additions, deletions, file changes, and commits.
        """
        nodes = raw_data['repository']['defaultBranchRef']['target']['history']['nodes']
        if cumulative_commits is None:
            cumulative_commits = {}
        
        # Process each commit node to accumulate data
        for node in nodes:
            # Consider only commits with less than 2 parents (usually mainline commits)
            if node['parents'] and node['parents']['totalCount'] < 2:
                name = node['author']['name']
                login = node['author']['user']
                if login:
                    login = login['login']
                additions = node['additions']
                deletions = node['deletions']
                files = node['changedFilesIfAvailable']
                if name not in cumulative_commits:
                    if login:
                        cumulative_commits[name] = {
                            login: {
                                'total_additions': additions,
                                'total_deletions': deletions,
                                'total_files': files,
                                'total_commits': 1
                            }
                        }
                    else:
                        cumulative_commits[name] = {
                            'total_additions': additions,
                            'total_deletions': deletions,
                            'total_files': files,
                            'total_commits': 1
                        }
                else:  # name in cumulative_commits
                    if login:
                        if login in cumulative_commits[name]:
                            cumulative_commits[name][login]['total_additions'] += additions
                            cumulative_commits[name][login]['total_deletions'] += deletions
                            cumulative_commits[name][login]['total_files'] += files
                            cumulative_commits[name][login]['total_commits'] += 1
                        else:  # login not in cumulative
                            cumulative_commits[name][login] = {
                                'total_additions': additions,
                                'total_deletions': deletions,
                                'total_files': files,
                                'total_commits': 1
                            }
                    else: # no login
                        if 'total_additions' in cumulative_commits[name]:
                            cumulative_commits[name]['total_additions'] += additions
                            cumulative_commits[name]['total_deletions'] += deletions
                            cumulative_commits[name]['total_files'] += files
                            cumulative_commits[name]['total_commits'] += 1
                        else:
                            cumulative_commits[name]['total_additions'] = additions
                            cumulative_commits[name]['total_deletions'] = deletions
                            cumulative_commits[name]['total_files'] = files
                            cumulative_commits[name]['total_commits'] = 1
        return cumulative_commits
