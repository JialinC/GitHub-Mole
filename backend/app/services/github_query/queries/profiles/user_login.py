"""The module defines several classes that formulate GraphQL query string to extract basic user profile information."""

from typing import Dict, Any
from ..query import QueryNode, Query
from ..constants import (
    NODE_VIEWER,
    NODE_USER,
    FIELD_LOGIN,
    FIELD_NAME,
    FIELD_ID,
    FIELD_EMAIL,
    FIELD_CREATED_AT,
    ARG_LOGIN,
    FIELD_BIO,
    FIELD_COMPANY,
    FIELD_TOTAL_COUNT,
    FIELD_AVATARURL,
    NODE_WATCHING,
    NODE_STARRED_REPOSITORIES,
    NODE_FOLLOWING,
    NODE_FOLLOWERS,
    NODE_ISSUES,
    NODE_PROJECTS,
    NODE_PULL_REQUESTS,
    NODE_REPOSITORIES,
    NODE_GIST_COMMENTS,
    NODE_ISSUE_COMMENTS,
    NODE_COMMIT_COMMENTS,
    NODE_REPOSITORY_DISCUSSION_COMMENTS,
    NODE_REPOSITORY_DISCUSSIONS,
    NODE_GISTS,
)


class UserLoginViewer(Query):
    """
    UserLoginViewer is a subclass of Query designed to fetch the viewer's login information using the 'viewer' field
    in a GraphQL query.
    """

    def __init__(self) -> None:
        """
        Initializes a UserLoginViewer object to fetch the current authenticated user's login name.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_VIEWER,
                    fields=[
                        FIELD_LOGIN,
                        FIELD_NAME,
                        FIELD_EMAIL,
                        FIELD_CREATED_AT,
                        FIELD_BIO,
                        FIELD_COMPANY,
                        FIELD_AVATARURL,
                        QueryNode(NODE_WATCHING, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(
                            NODE_STARRED_REPOSITORIES, fields=[FIELD_TOTAL_COUNT]
                        ),
                        QueryNode(NODE_FOLLOWING, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_FOLLOWERS, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_GISTS, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_ISSUES, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_PROJECTS, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_PULL_REQUESTS, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_REPOSITORIES, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(
                            NODE_REPOSITORY_DISCUSSIONS, fields=[FIELD_TOTAL_COUNT]
                        ),
                        QueryNode(NODE_GIST_COMMENTS, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_ISSUE_COMMENTS, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(NODE_COMMIT_COMMENTS, fields=[FIELD_TOTAL_COUNT]),
                        QueryNode(
                            NODE_REPOSITORY_DISCUSSION_COMMENTS,
                            fields=[FIELD_TOTAL_COUNT],
                        ),
                    ],
                )
            ]
        )

    @staticmethod
    def profile_stats(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes the raw data returned from a GraphQL query about a user's profile
        and extracts specific statistics. It formats the data into a more
        accessible and simplified dictionary structure.

        Args:
            raw_data (dict): The raw data returned by the query,
            expected to contain a 'user' key with nested user information.

        Returns:
            dict: A dictionary containing key statistics and information about the user, such as
            their login, creation date, company, number of followers, etc.
            Each piece of information is extracted from the nested structure of the
            input and presented as a flat dictionary for easier access.
        """
        profile_stats = raw_data[NODE_VIEWER]
        processed_stats = {
            "login": profile_stats[FIELD_LOGIN],
            "created_at": profile_stats[FIELD_CREATED_AT],
            "company": profile_stats[FIELD_COMPANY],
            "avatarUrl": profile_stats[FIELD_AVATARURL],
            "following": profile_stats[NODE_FOLLOWING][FIELD_TOTAL_COUNT],
            "followers": profile_stats[NODE_FOLLOWERS][FIELD_TOTAL_COUNT],
            "gists": profile_stats[NODE_GISTS][FIELD_TOTAL_COUNT],
            "issues": profile_stats[NODE_ISSUES][FIELD_TOTAL_COUNT],
            "projects": profile_stats[NODE_PROJECTS][FIELD_TOTAL_COUNT],
            "pull_requests": profile_stats[NODE_PULL_REQUESTS][FIELD_TOTAL_COUNT],
            "repositories": profile_stats[NODE_REPOSITORIES][FIELD_TOTAL_COUNT],
            "repository_discussions": profile_stats[
                NODE_REPOSITORY_DISCUSSION_COMMENTS
            ][FIELD_TOTAL_COUNT],
            "gist_comments": profile_stats[NODE_GIST_COMMENTS][FIELD_TOTAL_COUNT],
            "issue_comments": profile_stats[NODE_ISSUE_COMMENTS][FIELD_TOTAL_COUNT],
            "commit_comments": profile_stats[NODE_COMMIT_COMMENTS][FIELD_TOTAL_COUNT],
            "repository_discussion_comments": profile_stats[
                NODE_REPOSITORY_DISCUSSION_COMMENTS
            ][FIELD_TOTAL_COUNT],
            "watching": profile_stats[NODE_WATCHING][FIELD_TOTAL_COUNT],
            "starred_repositories": profile_stats[NODE_STARRED_REPOSITORIES][
                FIELD_TOTAL_COUNT
            ],
        }
        return processed_stats


class UserLogin(Query):
    """
    UserLogin is a subclass of Query designed to fetch a specific user's login and
    other profile information using the 'user' field in a GraphQL query.
    """

    def __init__(self, login: str) -> None:
        """
        Initializes a UserLogin object to fetch specified user information including login, name, id, email,
        and creation date.
        """
        super().__init__(
            fields=[
                QueryNode(
                    NODE_USER,
                    args={
                        ARG_LOGIN: login  # Variable to be substituted with actual user login.
                    },
                    fields=[
                        FIELD_LOGIN,  # The username or login name of the user.
                        FIELD_NAME,  # The full name of the user.
                        FIELD_ID,  # The unique ID of the user.
                        FIELD_EMAIL,  # The email address of the user.
                        FIELD_CREATED_AT,  # The creation date of the user's account.
                    ],
                )
            ]
        )
