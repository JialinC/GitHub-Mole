"""
This module defines a query class for fetching and processing a GitHub user's contribution calendar data
over a specified time range using GitHub's GraphQL API.

Classes:
    UserContributionCalendar: A class to construct and execute a query to fetch a user's contributions
                              and process the returned data into a structured format.

Functions:
    user_contribution_calendar: Static method to process raw data from the query and aggregate
                                the contributions into a countable collection.
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
    NODE_JOINED_GITHUB_CONTRIBUTION,
    NODE_CONTRIBUTION_CALENDAR,
    NODE_WEEKS,
    NODE_CONTRIBUTION_DAYS,
    FIELD_OCCURRED_AT,
    FIELD_DATE,
    FIELD_CONTRIBUTION_COUNT,
    FIELD_WEEKDAY,
    FIELD_CONTRIBUTION_YEARS,
)


class UserContributionCalendar(Query):
    """
    UserContributionCalendar constructs a GraphQL query to fetch the contribution history of a GitHub user.
    """

    def __init__(
        self,
        login: str,
        start: str = None,
        end: str = None,
    ) -> None:
        """
        Initializes a GraphQL query to retrieve user contribution data.

        Args:
            login (str): The GitHub username of the user.
            start (str): Optional start date for filtering contributions.
            end (str): Optional end date for filtering contributions.
        """

        time_args = {}
        if start:
            time_args[ARG_FROM] = start
        if end:
            time_args[ARG_TO] = end
        time_args = time_args if time_args else None

        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={ARG_LOGIN: login},
                    fields=[
                        QueryNode(
                            NODE_CONTRIBUTIONS_COLLECTION,
                            args=time_args,
                            fields=[
                                FIELD_STARTED_AT,
                                FIELD_ENDED_AT,
                                FIELD_CONTRIBUTION_YEARS,
                                QueryNode(
                                    NODE_JOINED_GITHUB_CONTRIBUTION,
                                    fields=[FIELD_OCCURRED_AT],
                                ),
                                QueryNode(
                                    NODE_CONTRIBUTION_CALENDAR,
                                    fields=[
                                        QueryNode(
                                            NODE_WEEKS,
                                            fields=[
                                                QueryNode(
                                                    NODE_CONTRIBUTION_DAYS,
                                                    fields=[
                                                        FIELD_DATE,
                                                        FIELD_CONTRIBUTION_COUNT,
                                                        FIELD_WEEKDAY,
                                                    ],
                                                )
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def user_contribution_calendar(raw_data: Dict[str, Any]) -> Counter:
        """
        Processes the raw data returned from a GraphQL query about a user's contributions collection.
        Extracts and organizes key contribution details.

        Args:
            raw_data (Dict[str, Any]): The raw response data retrieved from the GitHub GraphQL API.

        Returns:
            Tuple:
                - join_date (dict): The date the user first contributed on GitHub.
                - calendar (list): A structured list containing weekly contribution data.
                - years (list): A list of years during which the user has made contributions.
        """
        contributions = raw_data.get(NODE_USER, {}).get(
            NODE_CONTRIBUTIONS_COLLECTION, {}
        )
        join_date = contributions.get(NODE_JOINED_GITHUB_CONTRIBUTION, {})
        calendar = contributions.get(NODE_CONTRIBUTION_CALENDAR, {}).get(NODE_WEEKS, [])
        years = contributions.get(FIELD_CONTRIBUTION_YEARS, [])

        return join_date, calendar, years
