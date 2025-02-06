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
    UserContributionsCollection is a subclass of Query specifically designed to fetch a GitHub user's contributions
    over a certain period. It includes detailed contribution counts like commits, issues, pull requests, etc.
    """

    def __init__(
        self,
        login: str,
        start: str = None,
        end: str = None,
    ) -> None:
        """
        Initializes a UserContributionsCollection query object to fetch detailed contribution information of a user.
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
        Processes the raw data returned from a GraphQL query about a user's contributions collection
        and aggregates the various types of contributions into a countable collection.

        Args:
            raw_data (dict): The raw data returned by the query,
                            expected to contain nested contribution counts.

        Returns:
            Counter: A collection counter aggregating the various types of contributions made by the user.
        """
        contributions = raw_data.get(NODE_USER, {}).get(
            NODE_CONTRIBUTIONS_COLLECTION, {}
        )
        join_date = contributions.get(NODE_JOINED_GITHUB_CONTRIBUTION, {})
        calendar = contributions.get(NODE_CONTRIBUTION_CALENDAR, {}).get(NODE_WEEKS, [])
        years = contributions.get(FIELD_CONTRIBUTION_YEARS, [])

        return join_date, calendar, years
