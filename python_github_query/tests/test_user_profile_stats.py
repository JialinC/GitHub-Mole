import pytest
from python_github_query.queries.user_profile_stats import UserProfileStats


@pytest.mark.usefixtures("graphql_client")
class TestMetrics:
    def test_user_metrics_public(self):
        response = self.client.execute(
            query=UserProfileStats(), substitutions={"user": "JialinC"}
        )

        expected_data = {
            'user': {
                'login': 'JialinC',
                'name': 'Jialin Cui',
                'email': '',
                'createdAt': '2018-04-20T04:37:16Z',
                'bio': '\r\n    \r\n',
                'company': 'NC STATE',
                'isBountyHunter': False,
                'isCampusExpert': False,
                'isDeveloperProgramMember': False,
                'isEmployee': False,
                'isGitHubStar': False,
                'isHireable': True,
                'isSiteAdmin': False,
                'watching': {'totalCount': 15},
                'starredRepositories': {'totalCount': 5},
                'following': {'totalCount': 0},
                'followers': {'totalCount': 0},
                'gists': {'totalCount': 0},
                'gistComments': {'totalCount': 0},
                'issueComments': {'totalCount': 10},
                'issues': {'totalCount': 17},
                'projects': {'totalCount': 0},
                'pullRequests': {'totalCount': 36},
                'repositories': {'totalCount': 39},
                'repositoryDiscussionComments': {'totalCount': 0},
                'repositoryDiscussions': {'totalCount': 0}
            }
        }

        assert response == expected_data

    def test_user_metrics_enterprise(self):
        response = self.enterprise_client.execute(
            query=UserProfileStats(), substitutions={"user": "jcui9"}
        )

        expected_data = {
            'user': {
                'login': 'jcui9',
                'name': 'jcui9',
                'email': 'jcui9@ncsu.edu',
                'createdAt': '2019-09-11T17:08:06Z',
                'bio': '',
                'company': None,
                'isBountyHunter': False,
                'isCampusExpert': False,
                'isDeveloperProgramMember': False,
                'isEmployee': False,
                'isGitHubStar': False,
                'isHireable': False,
                'isSiteAdmin': False,
                'watching': {'totalCount': 11},
                'starredRepositories': {'totalCount': 0},
                'following': {'totalCount': 0},
                'followers': {'totalCount': 0},
                'gists': {'totalCount': 0},
                'gistComments': {'totalCount': 0},
                'issueComments': {'totalCount': 8},
                'issues': {'totalCount': 5},
                'projects': {'totalCount': 0},
                'pullRequests': {'totalCount': 2},
                'repositories': {'totalCount': 244},
                'repositoryDiscussionComments': {'totalCount': 0},
                'repositoryDiscussions': {'totalCount': 0}
            }
        }

        assert response == expected_data
