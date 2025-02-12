""""""

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
    # FIELD_AUTHORED_DATE,
    # FIELD_CHANGED_FILES_IF_AVAILABLE,
    # FIELD_ADDITIONS,
    # FIELD_DELETIONS,
    # FIELD_MESSAGE,
    # FIELD_NAME,
    # FIELD_EMAIL,
    # FIELD_LOGIN,
    # NODE_AUTHOR,
    # NODE_PARENTS,
    # NODE_USER,
)


class RepositoryBranchCommits(PaginatedQuery):
    """ """

    def __init__(
        self,
        owner: str,
        repo_name: str,
        branch_name: str,
        use_default: bool,
        pg_size: int = 50,
    ) -> None:
        """Initializes a paginated query for repository commits with specific fields and pagination controls."""

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
                                                                # FIELD_AUTHORED_DATE,
                                                                # FIELD_CHANGED_FILES_IF_AVAILABLE,
                                                                # FIELD_ADDITIONS,
                                                                # FIELD_DELETIONS,
                                                                # FIELD_MESSAGE,
                                                                # QueryNode(
                                                                #     NODE_PARENTS,
                                                                #     fields=[
                                                                #         FIELD_TOTAL_COUNT
                                                                #     ],
                                                                # ),
                                                                # QueryNode(
                                                                #     NODE_AUTHOR,
                                                                #     fields=[
                                                                #         FIELD_NAME,
                                                                #         FIELD_EMAIL,
                                                                #         QueryNode(
                                                                #             NODE_USER,
                                                                #             fields=[
                                                                #                 FIELD_LOGIN
                                                                #             ],
                                                                #         ),
                                                                #     ],
                                                                # ),
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

    # @staticmethod
    # def flatten_commit(commit: Dict[str, Any]) -> Dict[str, Any]:
    #     flattened = {}
    #     for key, value in commit.items():
    #         if key == "parents":
    #             flattened["parents"] = value[FIELD_TOTAL_COUNT]
    #         elif key == "author":
    #             flattened["author"] = value[FIELD_NAME]
    #             flattened["author_email"] = value[FIELD_EMAIL]
    #             if value[NODE_USER]:
    #                 flattened["author_login"] = value[NODE_USER][FIELD_LOGIN]
    #             else:
    #                 flattened["author_login"] = None
    #         else:
    #             flattened[key] = value
    #     return flattened

    # @staticmethod
    # def flatten_commits(commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    #     return [RepositoryBranchCommits.flatten_commit(commit) for commit in commits]

    # @staticmethod
    # def commits_stats(
    #     raw_data: Dict[str, Dict], cumulative_commits: Optional[Dict[str, Dict]] = None
    # ) -> Dict[str, Dict]:
    #     """
    #     Processes the raw data from the GraphQL query to accumulate commit data per author.

    #     Args:
    #         raw_data: The raw data returned from the GraphQL query.
    #         cumulative_commits: Optional cumulative commits dictionary to accumulate results.

    #     Returns:
    #         A dictionary of cumulative commit data per author, with details like total additions, deletions,
    #         file changes, and commits.
    #     """
    #     nodes = raw_data[NODE_REPOSITORY][NODE_REF][NODE_TARGET][NODE_HISTORY][
    #         NODE_NODES
    #     ]
    #     if cumulative_commits is None:
    #         cumulative_commits = {}

    #     # Process each commit node to accumulate data
    #     for node in nodes:
    #         # Consider only commits with less than 2 parents (usually mainline commits)
    #         if node[NODE_PARENTS] and node[NODE_PARENTS][FIELD_TOTAL_COUNT] < 2:
    #             name = node[NODE_AUTHOR][FIELD_NAME]
    #             login = node[NODE_AUTHOR][NODE_USER]
    #             if login:
    #                 login = login[FIELD_LOGIN]
    #             additions = node[FIELD_ADDITIONS]
    #             deletions = node[FIELD_DELETIONS]
    #             files = node[FIELD_CHANGED_FILES_IF_AVAILABLE]
    #             if name not in cumulative_commits:
    #                 if login:
    #                     cumulative_commits[name] = {
    #                         login: {
    #                             "total_additions": additions,
    #                             "total_deletions": deletions,
    #                             "total_files": files,
    #                             "total_commits": 1,
    #                         }
    #                     }
    #                 else:
    #                     cumulative_commits[name] = {
    #                         "total_additions": additions,
    #                         "total_deletions": deletions,
    #                         "total_files": files,
    #                         "total_commits": 1,
    #                     }
    #             else:  # name in cumulative_commits
    #                 if login:
    #                     if login in cumulative_commits[name]:
    #                         cumulative_commits[name][login][
    #                             "total_additions"
    #                         ] += additions
    #                         cumulative_commits[name][login][
    #                             "total_deletions"
    #                         ] += deletions
    #                         cumulative_commits[name][login]["total_files"] += files
    #                         cumulative_commits[name][login]["total_commits"] += 1
    #                     else:  # login not in cumulative
    #                         cumulative_commits[name][login] = {
    #                             "total_additions": additions,
    #                             "total_deletions": deletions,
    #                             "total_files": files,
    #                             "total_commits": 1,
    #                         }
    #                 else:  # no login
    #                     if "total_additions" in cumulative_commits[name]:
    #                         cumulative_commits[name]["total_additions"] += additions
    #                         cumulative_commits[name]["total_deletions"] += deletions
    #                         cumulative_commits[name]["total_files"] += files
    #                         cumulative_commits[name]["total_commits"] += 1
    #                     else:
    #                         cumulative_commits[name]["total_additions"] = additions
    #                         cumulative_commits[name]["total_deletions"] = deletions
    #                         cumulative_commits[name]["total_files"] = files
    #                         cumulative_commits[name]["total_commits"] = 1
    #     return cumulative_commits
