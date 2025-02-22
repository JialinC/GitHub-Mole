"""
This module defines the UserContributionsCollection class, which constructs a GraphQL query to fetch a GitHub user's 
contributions over a specified time period. The contributions include commits, issues, pull requests, pull request 
reviews, and repository contributions. The module also provides a method to process the raw data returned from the 
GraphQL query and extract the contribution counts.
Classes:
    UserContributionsCollection: Constructs a GraphQL query to retrieve user contributions and processes the raw data 
    to extract contribution counts.
Methods:
    __init__(login: str, start: str, end: str): Initializes the GraphQL query with the specified user login and time 
    range.
    user_contributions_collection(raw_data: Dict[str, Any]) -> Counter: Processes the raw data from the GraphQL API to 
    extract and count user contributions.
"""

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
    UserContributionsCollection constructs a GraphQL query to fetch a GitHub user's contributions
    over a given time period. It retrieves contributions such as commits, issues, pull requests, etc.
    """

    def __init__(
        self,
        login: str,
        start: str,
        end: str,
    ) -> None:
        """
        Initializes a GraphQL query to retrieve user contributions.

        Args:
            login (str): GitHub username.
            start (str): Start date for fetching contributions.
            end (str): End date for fetching contributions.
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
        Processes the raw data returned from a GraphQL query to extract contribution counts.

        Args:
            raw_data (dict): The response from the GraphQL API, containing user contribution data.

        Returns:
            Counter: Dictionary-like object with contribution counts.
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
