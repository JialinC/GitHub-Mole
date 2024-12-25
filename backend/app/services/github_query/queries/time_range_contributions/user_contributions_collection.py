"""The module defines the UserContributionsCollection class, which formulates the GraphQL query string
to extract the number of various contribution made by the user based on a given user ID."""

from typing import Dict, Any
from collections import Counter
from ..query import Query, QueryNode
from ..constants import (
    ARG_LOGIN,
    ARG_FROM,
    ARG_TO,
    NODE_USER,
    NODE_CONTRIBUTIONS_COLLECTION,
    FIELD_STARTED_AT,
    FIELD_ENDED_AT,
    FIELD_RESTRICTED_CONTRIBUTIONS_COUNT,
    FIELD_TOTAL_COMMIT_CONTRIBUTIONS,
    FIELD_TOTAL_ISSUE_CONTRIBUTIONS,
    FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS,
    FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS,
    FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS,
)


class UserContributionsCollection(Query):
    """
    UserContributionsCollection is a subclass of Query specifically designed to fetch a GitHub user's contributions
    over a certain period. It includes detailed contribution counts like commits, issues, pull requests, etc.
    """

    def __init__(
        self,
        login: str,
        start: str,
        end: str,
    ) -> None:
        """
        Initializes a UserContributionsCollection query object to fetch detailed contribution information of a user.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        QueryNode(
                            NODE_CONTRIBUTIONS_COLLECTION,
                            args={
                                ARG_FROM: start,
                                ARG_TO: end,
                            },
                            fields=[
                                FIELD_STARTED_AT,
                                FIELD_ENDED_AT,
                                FIELD_RESTRICTED_CONTRIBUTIONS_COUNT,
                                FIELD_TOTAL_COMMIT_CONTRIBUTIONS,
                                FIELD_TOTAL_ISSUE_CONTRIBUTIONS,
                                FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS,
                                FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS,
                                FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS,
                            ],
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def user_contributions_collection(raw_data: Dict[str, Any]) -> Counter:
        """
        Processes the raw data returned from a GraphQL query about a user's contributions collection
        and aggregates the various types of contributions into a countable collection.

        Args:
            raw_data (dict): The raw data returned by the query,
                            expected to contain nested contribution counts.

        Returns:
            Counter: A collection counter aggregating the various types of contributions made by the user.
        """
        raw_data = raw_data[NODE_USER][NODE_CONTRIBUTIONS_COLLECTION]
        contribution_collection = Counter(
            {
                "res_con": raw_data[FIELD_RESTRICTED_CONTRIBUTIONS_COUNT],
                "commit": raw_data[FIELD_TOTAL_COMMIT_CONTRIBUTIONS],
                "issue": raw_data[FIELD_TOTAL_ISSUE_CONTRIBUTIONS],
                "pr": raw_data[FIELD_TOTAL_PULL_REQUEST_CONTRIBUTIONS],
                "pr_review": raw_data[FIELD_TOTAL_PULL_REQUEST_REVIEW_CONTRIBUTIONS],
                "repository": raw_data[FIELD_TOTAL_REPOSITORY_CONTRIBUTIONS],
            }
        )
        return contribution_collection
