"""The module defines the RepositoryContributorsContribution class, which formulates the GraphQL query string
to extract all the commits made by a given contibutor to a repository's default branch."""

from typing import Dict, List, Optional, Any
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    ARG_FIRST,
    ARG_NAME,
    ARG_OWNER,
    ARG_AUTHOR,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    FIELD_TOTAL_COUNT,
    FIELD_AUTHORED_DATE,
    FIELD_CHANGED_FILES_IF_AVAILABLE,
    FIELD_ADDITIONS,
    FIELD_DELETIONS,
    FIELD_MESSAGE,
    FIELD_ID,
    NODE_DEFAULT_BRANCH_REF,
    NODE_HISTORY,
    NODE_NODES,
    NODE_PAGE_INFO,
    NODE_REPOSITORY,
    NODE_TARGET,
    NODE_ON,
    NODE_COMMIT,
    NODE_PARENTS,
)


class RepositoryContributorsContribution(PaginatedQuery):
    """
    RepositoryContributorsContribution is a subclass of PaginatedQuery specifically designed to fetch commits
    by a given contributor to a given repository's default branch.
    It locates the repository base on the owner GitHub ID and the repository's name.
    It locates the specific contributor using the unique GitHub universal identifier ID that can be fetched using
    the user profile query.
    """

    def __init__(
        self, owner: str, repo_name: str, GitHub_id: str, pg_size: int = 100
    ) -> None:
        """
        Initializes a paginated query to extract contributions made by contributors in a specific repository.
        Focuses on the commit history of the repository's default branch, targeting individual contributions.
        GitHub_id: str = "{ id: $id }"
        """
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
                            NODE_DEFAULT_BRANCH_REF,
                            fields=[
                                QueryNode(
                                    NODE_TARGET,
                                    fields=[
                                        QueryNode(
                                            NODE_ON + NODE_COMMIT,
                                            fields=[
                                                QueryNodePaginator(
                                                    NODE_HISTORY,
                                                    args={
                                                        ARG_AUTHOR: GitHub_id,
                                                        ARG_FIRST: pg_size,
                                                    },
                                                    fields=[
                                                        FIELD_TOTAL_COUNT,
                                                        QueryNode(
                                                            NODE_NODES,
                                                            fields=[
                                                                FIELD_ID,
                                                                FIELD_AUTHORED_DATE,
                                                                FIELD_CHANGED_FILES_IF_AVAILABLE,
                                                                FIELD_ADDITIONS,
                                                                FIELD_DELETIONS,
                                                                FIELD_MESSAGE,
                                                                QueryNode(
                                                                    NODE_PARENTS,
                                                                    fields=[
                                                                        FIELD_TOTAL_COUNT
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
    def user_cumulated_contribution(
        raw_data: Dict[str, Any],
        cumulative_contribution: Optional[Dict[str, int]] = None,
    ) -> Dict[str, int]:
        """
        Calculates cumulative contribution statistics of a user from the provided raw data.

        Args:
            raw_data (Dict): Raw data returned by the GraphQL query.
            cumulative_contribution (Optional[Dict[str, int]]): A dictionary to accumulate contributions.
                                                               If None, a new dictionary is initialized.

        Returns:
            Dict[str, int]: A dictionary containing the cumulative statistics: total additions, deletions, and commits.
        """
        nodes = raw_data[NODE_REPOSITORY][NODE_DEFAULT_BRANCH_REF][NODE_TARGET][
            NODE_HISTORY
        ][NODE_NODES]
        if cumulative_contribution is None:
            cumulative_contribution = {
                "total_additions": 0,
                "total_deletions": 0,
                "total_commits": 0,
            }

        for node in nodes:
            if node[NODE_PARENTS] and node[NODE_PARENTS][FIELD_TOTAL_COUNT] < 2:
                cumulative_contribution["total_additions"] += node[FIELD_ADDITIONS]
                cumulative_contribution["total_deletions"] += node[FIELD_DELETIONS]
                cumulative_contribution["total_commits"] += 1

        return cumulative_contribution

    @staticmethod
    def user_commit_contribution(
        raw_data: Dict[str, Any],
        commit_contributions: Optional[List[Dict[str, int]]] = None,
    ) -> List[Dict[str, int]]:
        """
        Extracts and compiles individual commit contributions from the raw data.

        Args:
            raw_data (Dict): Raw data returned by the GraphQL query.
            commit_contributions (Optional[List[Dict[str, int]]]): A list to accumulate individual commit contributions.

        Returns:
            List[Dict[str, int]]: A list of dictionaries, each representing details of an individual commit.
        """
        nodes = raw_data[NODE_REPOSITORY][NODE_DEFAULT_BRANCH_REF][NODE_TARGET][
            NODE_HISTORY
        ][NODE_NODES]
        if commit_contributions is None:
            commit_contributions = []

        for node in nodes:
            if node[NODE_PARENTS] and node[NODE_PARENTS][FIELD_TOTAL_COUNT] < 2:
                commit_contributions.append(
                    {
                        "authoredDate": node[FIELD_AUTHORED_DATE],
                        "changedFiles": node[FIELD_CHANGED_FILES_IF_AVAILABLE],
                        "additions": node[FIELD_ADDITIONS],
                        "deletions": node[FIELD_DELETIONS],
                        "message": node[FIELD_MESSAGE],
                    }
                )

        return commit_contributions
