import pytest
from python_github_query.queries.user_contributions_collection import UserContributionsCollection


@pytest.mark.usefixtures("graphql_client")
class TestUserContributionsCollection:
    def test_user_commits_public(self):
        response = self.client.execute(
            query=UserContributionsCollection(), substitutions={"user": "JialinC",
                                                "start": "2020-02-07T18:11:20Z",
                                                "end": "2021-02-07T18:11:20Z"}
        )

        expected_data = {
            'user': {
                'contributionsCollection': {
                    'startedAt': '2020-02-07T18:11:20Z',
                    'endedAt': '2021-02-07T18:11:20Z',
                    'hasActivityInThePast': True,
                    'hasAnyContributions': True,
                    'hasAnyRestrictedContributions': False,
                    'restrictedContributionsCount': 0,
                    'totalCommitContributions': 72,
                    'totalIssueContributions': 9,
                    'totalPullRequestContributions': 29,
                    'totalPullRequestReviewContributions': 0,
                    'totalRepositoriesWithContributedCommits': 7,
                    'totalRepositoriesWithContributedIssues': 2,
                    'totalRepositoriesWithContributedPullRequestReviews': 0,
                    'totalRepositoriesWithContributedPullRequests': 11,
                    'totalRepositoryContributions': 11
                }
            }
        }

        assert response == expected_data

    def test_user_commits_enterprise(self):
        response = self.enterprise_client.execute(
            query=UserContributionsCollection(), substitutions={"user": "jcui9",
                                                "start": "2020-02-07T18:11:20Z",
                                                "end": "2021-02-07T18:11:20Z"}
        )

        expected_data = {
            'user': {
                'contributionsCollection': {
                    'startedAt': '2020-02-07T18:11:20Z',
                    'endedAt': '2021-02-07T18:11:20Z',
                    'hasActivityInThePast': True,
                    'hasAnyContributions': True,
                    'hasAnyRestrictedContributions': False,
                    'restrictedContributionsCount': 0,
                    'totalCommitContributions': 1,
                    'totalIssueContributions': 5,
                    'totalPullRequestContributions': 0,
                    'totalPullRequestReviewContributions': 0,
                    'totalRepositoriesWithContributedCommits': 1,
                    'totalRepositoriesWithContributedIssues': 1,
                    'totalRepositoriesWithContributedPullRequestReviews': 0,
                    'totalRepositoriesWithContributedPullRequests': 0,
                    'totalRepositoryContributions': 4
                }
            }
        }

        assert response == expected_data


