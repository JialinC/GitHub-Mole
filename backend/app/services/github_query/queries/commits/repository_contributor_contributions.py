"""
This module defines the RepositoryContributorContributions class, which is a subclass of PaginatedQuery.
It is designed to fetch commit contributions made by a specific contributor to a repository's default branch on GitHub.
The module includes methods to format GitHub IDs, extract commit lists, flatten commit data, and calculate cumulative
and individual commit contributions.

Classes:
    RepositoryContributorContributions: A class to query and process commit contributions of a specific user in a
    repository.

Functions:
   commits_list(raw_data: Dict[str, Dict]) -> Dict[str, Dict]:
   flatten_commit(commit: Dict[str, Any]) -> Dict[str, Any]:
   flatten_commits(commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
   user_cumulated_contribution(raw_data: Dict[str, Any], cumulative_contribution: Optional[Dict[str, int]] = None,
    ) -> Dict[str, int]:
   user_commit_contribution(raw_data: Dict[str, Any], commit_contributions: Optional[List[Dict[str, int]]] = None,
    ) -> List[Dict[str, int]]:
"""

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
    FIELD_OID,
    NODE_DEFAULT_BRANCH_REF,
    NODE_HISTORY,
    NODE_NODES,
    NODE_PAGE_INFO,
    NODE_REPOSITORY,
    NODE_TARGET,
    NODE_ON,
    NODE_COMMIT,
    NODE_PARENTS,
    NODE_REF,
    ARG_QUALIFIED_NAME,
    FIELD_NAME,
    FIELD_EMAIL,
    NODE_USER,
    FIELD_LOGIN,
)


def format_github_id(github_id: str) -> dict:
    """
    Formats a GitHub ID into a dictionary with the key "id" and the value as the GitHub ID
    enclosed in double quotes.

    Args:
        github_id (str): The GitHub ID to format.

    Returns:
        dict: A dictionary with the formatted GitHub ID.
    """
    return {"id": f'"{github_id}"'}


class RepositoryContributorContributions(PaginatedQuery):
    """
    RepositoryContributorContributions is a paginated GraphQL query
    designed to fetch commits made by a specific contributor to a repository.
    """

    def __init__(
        self,
        owner: str,
        repo_name: str,
        branch_name: str,
        github_id: str,
        pg_size: int = 50,
    ) -> None:
        """
        Initializes a paginated query to retrieve commit contributions.

        Args:
            owner (str): Repository owner.
            repo_name (str): Repository name.
            branch_name (str): Branch name.
            github_id (str): GitHub ID of the contributor.
            pg_size (int): Number of commits per page.
        """
        github_id = format_github_id(github_id)
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
                            NODE_REF,
                            args={ARG_QUALIFIED_NAME: branch_name},
                            fields=[
                                QueryNode(
                                    NODE_TARGET,
                                    fields=[
                                        QueryNode(
                                            NODE_ON
                                            + NODE_COMMIT,  # Inline fragment on Commit type
                                            fields=[
                                                QueryNodePaginator(
                                                    NODE_HISTORY,
                                                    args={
                                                        ARG_AUTHOR: github_id,
                                                        ARG_FIRST: pg_size,
                                                    },
                                                    fields=[
                                                        FIELD_TOTAL_COUNT,
                                                        QueryNode(
                                                            NODE_NODES,
                                                            fields=[FIELD_OID],
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
    def commits_list(raw_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Extracts the commit history nodes from the raw data.

        Args: raw_data (Dict[str, Dict]): The raw data containing repository information.

        Returns: Dict[str, Dict]: The commit history nodes extracted from the raw data.

        """
        nodes = raw_data[NODE_REPOSITORY][NODE_REF][NODE_TARGET][NODE_HISTORY]
        return nodes

    @staticmethod
    def flatten_commit(commit: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flattens a commit dictionary by extracting specific fields and transforming nested structures.

        Args:
            commit (Dict[str, Any]): A dictionary representing a commit with nested structures.

        Returns:
            Dict[str, Any]: A flattened dictionary with specific fields extracted and transformed.
                - "parents": The total count of parent commits.
                - "author": The name of the author.
                - "author_email": The email of the author.
                - "author_id": The login ID of the author if available, otherwise None.
                - "author_login": The login of the author if available, otherwise None.
                - Other keys and values from the original commit dictionary are included as is.
        """
        flattened = {}
        for key, value in commit.items():
            if key == "parents":
                flattened["parents"] = value[FIELD_TOTAL_COUNT]
            elif key == "author":
                flattened["author"] = value[FIELD_NAME]
                flattened["author_email"] = value[FIELD_EMAIL]
                if value[NODE_USER]:
                    flattened["author_id"] = value[NODE_USER][FIELD_LOGIN]
                else:
                    flattened["author_login"] = None
            else:
                flattened[key] = value
        return flattened

    @staticmethod
    def flatten_commits(commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Flattens a list of commit dictionaries.

        This function takes a list of commit dictionaries and flattens each commit
        using the `flatten_commit` method from the `RepositoryContributorContributions` class.

        Args:
            commits (List[Dict[str, Any]]): A list of commit dictionaries to be flattened.

        Returns:
            List[Dict[str, Any]]: A list of flattened commit dictionaries.
        """
        return [
            RepositoryContributorContributions.flatten_commit(commit)
            for commit in commits
        ]

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
