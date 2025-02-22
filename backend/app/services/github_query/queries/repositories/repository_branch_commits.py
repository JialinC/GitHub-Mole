"""
This module defines a class for querying commit history from a specific branch of a GitHub repository using GraphQL.

Classes:
    RepositoryBranchCommits: A class to create and manage paginated queries for retrieving commit history from a
    specified branch of a GitHub repository.

Functions:
    __init__: Initializes the RepositoryBranchCommits class with repository details and pagination settings.
    commits_list: Extracts commit history from raw GraphQL response data.
"""

from typing import Dict  # , List, Optional, Any
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    ARG_FIRST,
    ARG_NAME,
    ARG_OWNER,
    ARG_QUALIFIED_NAME,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    FIELD_TOTAL_COUNT,
    FIELD_OID,
    NODE_REF,
    NODE_DEFAULT_BRANCH_REF,
    NODE_HISTORY,
    NODE_NODES,
    NODE_PAGE_INFO,
    NODE_REPOSITORY,
    NODE_TARGET,
    NODE_ON,
    NODE_COMMIT,
)


class RepositoryBranchCommits(PaginatedQuery):
    """
    RepositoryBranchCommits fetches the commit history for a given repository branch.
    It extends PaginatedQuery to handle potentially large numbers of commits.
    """

    def __init__(
        self,
        owner: str,
        repo_name: str,
        branch_name: str,
        use_default: bool,
        pg_size: int = 50,
    ) -> None:
        """
        Initializes a paginated query for repository commits.

        Args:
            owner (str): The GitHub username or organization name.
            repo_name (str): The repository name.
            branch_name (str): The branch name (ignored if use_default=True).
            use_default (bool): Whether to fetch commits from the default branch.
            pg_size (int): The number of commits to retrieve per page.
        """

        self.branch_node = NODE_DEFAULT_BRANCH_REF if use_default else NODE_REF
        branch_args = None if use_default else {ARG_QUALIFIED_NAME: branch_name}
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
                            self.branch_node,
                            args=branch_args,
                            fields=[
                                QueryNode(
                                    NODE_TARGET,
                                    fields=[
                                        QueryNode(
                                            NODE_ON + NODE_COMMIT,
                                            fields=[
                                                QueryNodePaginator(
                                                    NODE_HISTORY,
                                                    args={ARG_FIRST: pg_size},
                                                    fields=[
                                                        FIELD_TOTAL_COUNT,
                                                        QueryNode(
                                                            NODE_NODES,
                                                            fields=[
                                                                FIELD_OID,
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

    def commits_list(self, raw_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Extracts commit history from raw GraphQL response data.

        Args:
            raw_data (Dict[str, Dict]): The API response data.

        Returns:
            Dict[str, Dict]: The extracted commit nodes.
        """
        return raw_data[NODE_REPOSITORY][self.branch_node][NODE_TARGET][NODE_HISTORY]
