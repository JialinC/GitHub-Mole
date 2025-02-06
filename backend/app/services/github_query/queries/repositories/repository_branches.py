""""""

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
    """ """

    def __init__(
        self,
        owner: str,
        repo_name: str,
        prefix: str = '"refs/heads/"',
        pg_size: int = 10,
    ) -> None:
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
        Extracts issues from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of issues, each represented as a dictionary.
        """
        return raw_data.get(NODE_REPOSITORY, {}).get(NODE_REFS, {})
