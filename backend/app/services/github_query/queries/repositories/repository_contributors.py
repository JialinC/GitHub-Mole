"""The module defines the RepositoryContributors class, which formulates the GraphQL query string
to extract all contibutors to a repository's default branch."""

from typing import Dict, Set, Optional
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
    FIELD_LOGIN,
    FIELD_EMAIL,
    FIELD_NAME,
    FIELD_TOTAL_COUNT,
    NODE_AUTHOR,
    NODE_DEFAULT_BRANCH_REF,
    NODE_HISTORY,
    NODE_NODES,
    NODE_PAGE_INFO,
    NODE_REPOSITORY,
    NODE_TARGET,
    NODE_USER,
    NODE_ON,
    NODE_COMMIT,
)


class RepositoryContributors(PaginatedQuery):
    """
    RepositoryContributors is a subclass of PaginatedQuery specifically designed to fetch contributors' information to
    of a given repository's default branch.
    It locates the repository base on the owner GitHub ID and the repository's name.
    """

    def __init__(self, owner: str, repo_name: str, pg_size: int = 50) -> None:
        super().__init__(
            fields=[
                QueryNode(
                    NODE_REPOSITORY,
                    args={
                        ARG_OWNER: owner,
                        ARG_NAME: repo_name,
                    },  # Query arguments for specifying the repository
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
                                                    args={ARG_FIRST: pg_size},
                                                    fields=[
                                                        FIELD_TOTAL_COUNT,  # Total number of commits in the history
                                                        QueryNode(
                                                            NODE_NODES,  # List of commit nodes
                                                            fields=[
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
                                                                )
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
    def extract_unique_author(
        raw_data: Dict[str, Dict], unique_authors: Optional[Dict[str, Set[str]]] = None
    ) -> Dict[str, Set[str]]:
        """
        Processes the raw data from the GraphQL query to extract unique authors from the repository's commit history.

        Args:
            raw_data: The raw data returned from the GraphQL query.
            unique_authors: An optional dictionary to accumulate unique authors' names and logins.

        Returns:
            A dictionary containing sets of unique author names and logins.
        """
        nodes = raw_data[NODE_REPOSITORY][NODE_DEFAULT_BRANCH_REF][NODE_TARGET][
            NODE_HISTORY
        ][NODE_NODES]
        if unique_authors is None:
            unique_authors = {"name": set(), "login": set()}

        # Process each commit node to accumulate unique author data
        for node in nodes:
            author = node[NODE_AUTHOR]
            name = author[FIELD_NAME]
            login = author[NODE_USER][FIELD_LOGIN] if author[NODE_USER] else None

            if name:
                unique_authors[FIELD_NAME].add(name)
            if login:
                unique_authors[FIELD_LOGIN].add(login)

        return unique_authors
