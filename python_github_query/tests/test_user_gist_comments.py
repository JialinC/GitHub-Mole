import pytest
from python_github_query.queries.comments.user_gist_comments import UserGistComments


@pytest.mark.usefixtures("graphql_client")
class TestUserGistComments:
    def test_user_gist_comments_public(self):
        expected_data = {
            'user': {
                'login': 'JialinC',
                'gistComments': {
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
        for response in self.client.execute(query=UserGistComments(),
                                            substitutions={"user": "JialinC", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_gist_comments_enterprise(self):
        expected_data = {
            'user': {
                'login': 'jcui9',
                'gistComments': {
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
        for response in self.enterprise_client.execute(query=UserGistComments(),
                                                       substitutions={"user": "jcui9", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1
