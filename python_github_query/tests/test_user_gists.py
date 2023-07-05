import pytest
from python_github_query.queries.user_gists import UserGists


@pytest.mark.usefixtures("graphql_client")
class TestUserGists:
    def test_user_gists_public(self):
        expected_data = {'user': {
            'login': 'JialinC',
            'gists': {
                'totalCount': 0,
                'nodes': [],
                'pageInfo': {'endCursor': None, 'hasNextPage': False}}}}
        count = 0
        for response in self.client.execute(query=UserGists(),
                                            substitutions={"user": "JialinC", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_gists_enterprise(self):
        expected_data = {'user': {
            'login': 'jcui9',
            'gists': {
                'totalCount': 0,
                'nodes': [],
                'pageInfo': {'endCursor': None, 'hasNextPage': False}}}}
        count = 0
        for response in self.enterprise_client.execute(query=UserGists(),
                                                       substitutions={"user": "jcui9", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1
