"""The module defines the RepositoryCommits class, which formulates the GraphQL query string
to extract all the commits made to a repository's default branch."""

from typing import Dict, Optional
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    ARG_FIRST,
    ARG_NAME,
    ARG_OWNER,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    FIELD_TOTAL_COUNT,
    FIELD_AUTHORED_DATE,
    FIELD_CHANGED_FILES_IF_AVAILABLE,
    FIELD_ADDITIONS,
    FIELD_DELETIONS,
    FIELD_MESSAGE,
    FIELD_ID,
    FIELD_NAME,
    FIELD_EMAIL,
    FIELD_LOGIN,
    NODE_AUTHOR,
    NODE_DEFAULT_BRANCH_REF,
    NODE_HISTORY,
    NODE_NODES,
    NODE_PAGE_INFO,
    NODE_REPOSITORY,
    NODE_TARGET,
    NODE_ON,
    NODE_COMMIT,
    NODE_PARENTS,
    NODE_USER,
)


class RepositoryCommits(PaginatedQuery):
    """
    RepositoryCommits is a subclass of PaginatedQuery specifically designed to fetch commits to a given repository.
    It includes authoredDate, changedFilesIfAvailable, additions, deletions,  and message.
    It locates the repository base on the owner GitHub ID and the repository's name.
    """

    def __init__(self, owner: str, repo_name: str, pg_size: int = 10) -> None:
        """Initializes a paginated query for repository commits with specific fields and pagination controls."""
        super().__init__(
            fields=[
                QueryNode(
                    NODE_REPOSITORY,
                    args={
                        ARG_OWNER: owner,
                        ARG_NAME: repo_name,
                    },
                    fields=[
                        QueryNode(
                            NODE_DEFAULT_BRANCH_REF,  # Points to the default branch of the repository
                            fields=[
                                QueryNode(
                                    NODE_TARGET,
                                    fields=[
                                        QueryNode(
                                            NODE_ON
                                            + NODE_COMMIT,  # Inline fragment on Commit type
                                            fields=[
                                                QueryNodePaginator(
                                                    NODE_HISTORY,  # Paginated history of commits
                                                    args={
                                                        ARG_FIRST: pg_size
                                                    },  # Pagination control arguments
                                                    fields=[
                                                        FIELD_TOTAL_COUNT,  # Total number of commits in the history
                                                        QueryNode(
                                                            NODE_NODES,  # List of commit nodes
                                                            fields=[
                                                                FIELD_ID,
                                                                # Date when the commit was authored
                                                                FIELD_AUTHORED_DATE,
                                                                # Number of files changed, if available
                                                                FIELD_CHANGED_FILES_IF_AVAILABLE,
                                                                # Number of additions made in the commit
                                                                FIELD_ADDITIONS,
                                                                # Number of deletions made in the commit
                                                                FIELD_DELETIONS,
                                                                # Commit message
                                                                FIELD_MESSAGE,
                                                                QueryNode(
                                                                    # Parent commits of the commit, limited to 2
                                                                    NODE_PARENTS,
                                                                    fields=[
                                                                        FIELD_TOTAL_COUNT  # Total number of parents
                                                                    ],
                                                                ),
                                                                QueryNode(
                                                                    NODE_AUTHOR,  # Author of the commit
                                                                    fields=[
                                                                        FIELD_NAME,  # Name of the author
                                                                        FIELD_EMAIL,  # Email of the author
                                                                        QueryNode(
                                                                            NODE_USER,
                                                                            fields=[
                                                                                FIELD_LOGIN  # Login of the user
                                                                            ],
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        QueryNode(
                                                            NODE_PAGE_INFO,
                                                            fields=[
                                                                FIELD_END_CURSOR,
                                                                FIELD_HAS_NEXT_PAGE,
                                                            ],
                                                        ),
                                                    ],
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ]
        )

    @staticmethod
    def commits_list(
        raw_data: Dict[str, Dict], cumulative_commits: Optional[Dict[str, Dict]] = None
    ) -> Dict[str, Dict]:
        """
        Processes the raw data from the GraphQL query to accumulate commit data per author.

        Args:
            raw_data: The raw data returned from the GraphQL query.
            cumulative_commits: Optional cumulative commits dictionary to accumulate results.

        Returns:
            A dictionary of cumulative commit data per author, with details like total additions, deletions,
            file changes, and commits.
        """
        nodes = raw_data[NODE_REPOSITORY][NODE_DEFAULT_BRANCH_REF][NODE_TARGET][
            NODE_HISTORY
        ][NODE_NODES]
        if cumulative_commits is None:
            cumulative_commits = {}

        # Process each commit node to accumulate data
        for node in nodes:
            # Consider only commits with less than 2 parents (usually mainline commits)
            if node[NODE_PARENTS] and node[NODE_PARENTS][FIELD_TOTAL_COUNT] < 2:
                name = node[NODE_AUTHOR][FIELD_NAME]
                login = node[NODE_AUTHOR][NODE_USER]
                if login:
                    login = login[FIELD_LOGIN]
                additions = node[FIELD_ADDITIONS]
                deletions = node[FIELD_DELETIONS]
                files = node[FIELD_CHANGED_FILES_IF_AVAILABLE]
                if name not in cumulative_commits:
                    if login:
                        cumulative_commits[name] = {
                            login: {
                                "total_additions": additions,
                                "total_deletions": deletions,
                                "total_files": files,
                                "total_commits": 1,
                            }
                        }
                    else:
                        cumulative_commits[name] = {
                            "total_additions": additions,
                            "total_deletions": deletions,
                            "total_files": files,
                            "total_commits": 1,
                        }
                else:  # name in cumulative_commits
                    if login:
                        if login in cumulative_commits[name]:
                            cumulative_commits[name][login][
                                "total_additions"
                            ] += additions
                            cumulative_commits[name][login][
                                "total_deletions"
                            ] += deletions
                            cumulative_commits[name][login]["total_files"] += files
                            cumulative_commits[name][login]["total_commits"] += 1
                        else:  # login not in cumulative
                            cumulative_commits[name][login] = {
                                "total_additions": additions,
                                "total_deletions": deletions,
                                "total_files": files,
                                "total_commits": 1,
                            }
                    else:  # no login
                        if "total_additions" in cumulative_commits[name]:
                            cumulative_commits[name]["total_additions"] += additions
                            cumulative_commits[name]["total_deletions"] += deletions
                            cumulative_commits[name]["total_files"] += files
                            cumulative_commits[name]["total_commits"] += 1
                        else:
                            cumulative_commits[name]["total_additions"] = additions
                            cumulative_commits[name]["total_deletions"] = deletions
                            cumulative_commits[name]["total_files"] = files
                            cumulative_commits[name]["total_commits"] = 1
        return cumulative_commits
