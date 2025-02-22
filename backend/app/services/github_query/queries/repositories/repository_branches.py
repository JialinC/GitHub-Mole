"""
This module defines the `RepositoryBranches` class, which is used to query and extract branch information
from a GitHub repository using the GitHub GraphQL API.
Classes:
    RepositoryBranches: A class to perform paginated queries to fetch branches of a specified repository.
Functions:
    branches(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]: Extracts branches from the raw data returned by a
    GraphQL query.
"""

from typing import List, Dict, Any
from ..query import (
    QueryNode,
    PaginatedQuery,
    QueryNodePaginator,
)
from ..constants import (
    ARG_FIRST,
    ARG_NAME,
    ARG_OWNER,
    ARG_REF_PREFIX,
    FIELD_END_CURSOR,
    FIELD_HAS_NEXT_PAGE,
    FIELD_TOTAL_COUNT,
    FIELD_NAME,
    NODE_REPOSITORY,
    NODE_REFS,
    NODE_NODES,
    NODE_PAGE_INFO,
)


class RepositoryBranches(PaginatedQuery):
    """
    RepositoryBranches is a class for querying repository branches.
    It extends PaginatedQuery to handle potentially large numbers of branches.
    """

    def __init__(
        self,
        owner: str,
        repo_name: str,
        prefix: str = '"refs/heads/"',
        pg_size: int = 50,
    ) -> None:
        """
        Initializes a paginated query for fetching GitHub repository branches.

        Args:
            owner (str): GitHub username or organization that owns the repository.
            repo_name (str): The name of the repository.
            prefix (str, optional): Prefix for branch references (default: "refs/heads/").
            pg_size (int, optional): Number of branches to fetch per request (default: 50).

        Returns:
            None: Constructs a GraphQL query to fetch repository branches.

        Raises:
            QueryFailedException: If the GraphQL query fails.
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
                        QueryNodePaginator(
                            NODE_REFS,
                            args={ARG_REF_PREFIX: prefix, ARG_FIRST: pg_size},
                            fields=[
                                FIELD_TOTAL_COUNT,
                                QueryNode(
                                    NODE_NODES,
                                    fields=[FIELD_NAME],
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
            ]
        )

    @staticmethod
    def branches(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts branches from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of branches.
        """
        return raw_data.get(NODE_REPOSITORY, {}).get(NODE_REFS, {})
