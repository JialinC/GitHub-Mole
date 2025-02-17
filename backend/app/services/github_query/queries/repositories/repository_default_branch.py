""""""

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
    """ """

    def __init__(
        self,
        owner: str,
        repo_name: str,
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
        Extracts issues from the raw data returned by a GraphQL query.

        Args:
            raw_data (Dict): The raw data returned from the GraphQL query.

        Returns:
            List[Dict]: A list of issues, each represented as a dictionary.
        """
        default_branch = raw_data.get(NODE_REPOSITORY, {}).get(
            NODE_DEFAULT_BRANCH_REF, {}
        )
        return default_branch if default_branch else {}
