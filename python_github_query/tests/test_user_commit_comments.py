import pytest
from python_github_query.queries.user_commit_comments import UserCommitComments


@pytest.mark.usefixtures("graphql_client")
class TestUserCommitComments:
    def test_user_commit_comments_public(self):
        expected_data = {
            'user': {
                'login': 'JialinC',
                'commitComments': {
                    'totalCount': 1,
                    'nodes': [{'body': 'Great contribution:)',
                               'createdAt': '2022-02-09T00:52:50Z'}],
                    'pageInfo': {
                        'endCursor': 'Y3Vyc29yOnYyOpHOA_OXWw==',
                        'hasNextPage': False
                    }
                }
            }
        }
        count = 0
        for response in self.client.execute(query=UserCommitComments(),
                                            substitutions={"user": "JialinC", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_commit_comments_enterprise(self):
        expected_data = {
            'user': {
                'login': 'jcui9',
                'commitComments': {
                    'totalCount': 0,
                    'nodes': [],
                    'pageInfo': {
                        'endCursor': None,
                        'hasNextPage': False
                    }
                }
            }
        }
        count = 0
        for response in self.enterprise_client.execute(query=UserCommitComments(),
                                                       substitutions={"user": "jcui9", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

