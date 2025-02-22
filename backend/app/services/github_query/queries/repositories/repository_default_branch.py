"""
This module defines a GraphQL query for retrieving the default branch of a GitHub repository.

Classes:
    RepositoryDefaultBranch: A class to construct and execute a GraphQL query to fetch the default branch of a
    specified repository.

Functions:
    default_branch: A static method to extract the default branch information from the raw data returned by the GraphQL
    query.
"""

from typing import List, Dict, Any
from ..query import Query, QueryNode
from ..constants import (
    ARG_NAME,
    ARG_OWNER,
    FIELD_NAME,
    NODE_DEFAULT_BRANCH_REF,
    NODE_REPOSITORY,
)


class RepositoryDefaultBranch(Query):
    """
    RepositoryDefaultBranch is a class for querying a repository's default branch.
    """

    def __init__(
        self,
        owner: str,
        repo_name: str,
    ) -> None:
        """
        Initializes a GraphQL query to retrieve the default branch of a repository.

        Args:
            owner (str): The GitHub username or organization that owns the repository.
            repo_name (str): The name of the repository.
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
                            fields=[FIELD_NAME],
                        ),
                    ],
                ),
            ],
        )

    @staticmethod
    def default_branch(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extracts the default branch from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            Dict: A dictionary containing the default branch name.
        """
        default_branch = raw_data.get(NODE_REPOSITORY, {}).get(
            NODE_DEFAULT_BRANCH_REF, {}
        )
        return default_branch if default_branch else {}
