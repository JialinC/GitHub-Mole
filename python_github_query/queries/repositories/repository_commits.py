from python_github_query.github_graphql.query import QueryNode, PaginatedQuery, QueryNodePaginator


class RepositoryCommits(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "repository",
                    args={"owner": "$owner",
                          "name": "$repo_name"},
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
                                                    args={"first": "$pg_size"},
                                                    fields=[
                                                        'totalCount',
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
                                                                    fields=[
                                                                        "totalCount"
                                                                    ]
                                                                ),
                                                                QueryNode(
                                                                    "author",
                                                                    fields=[
                                                                        'name',
                                                                        'email',
                                                                        QueryNode(
                                                                            "user",
                                                                            fields=[
                                                                                "login"
                                                                            ]
                                                                        )
                                                                    ]
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
    def commits_list(raw_data: dict, cumulative_commits: dict = None):
        """
        Return the cumulated contribution of the contributor
        Args:
            raw_data: the raw data returned by the query
            cumulative_commits: cumulative commits dict
        Returns:
            list: a list of contributor's total additions, total deletions, and total number of commits.
            [total_commits, total_additions, total_deletions]
        """
        nodes = raw_data['repository']['defaultBranchRef']['target']['history']['nodes']
        if cumulative_commits is None:
            cumulative_commits = {}
        for node in nodes:
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
                    else:  # no login
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
