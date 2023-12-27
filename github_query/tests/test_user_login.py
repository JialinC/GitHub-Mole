import pytest
from github_query.queries.profile.user_login import UserLoginViewer, UserLogin


@pytest.mark.usefixtures("graphql_client")
class TestLogin:
    def test_user_login_viewer_public(self):
        response = self.client.execute(
            query=UserLoginViewer(), substitutions={}
        )

        expected_data = {
            'viewer': {
                'login': 'JialinC'
            }
        }
        assert response == expected_data

    def test_user_login_viewer_enterprise(self):
        response = self.enterprise_client.execute(
            query=UserLoginViewer(), substitutions={}
        )

        expected_data = {
            'viewer': {
                'login': 'jcui9'
            }
        }
        assert response == expected_data

    def test_user_login_public(self):
        response = self.client.execute(
            query=UserLogin(), substitutions={"user": "JialinC"}
        )

        expected_data = {
            'user': {
                'login': 'JialinC',
                'name': 'Jialin Cui',
                "id": 'MDQ6VXNlcjM4NTQ5Njg5',
                'email': '',
                'createdAt': '2018-04-20T04:37:16Z'}
        }
        assert response == expected_data

    def test_user_login_enterprise(self, graphql_client):
        response = self.enterprise_client.execute(
            query=UserLogin(), substitutions={"user": "jcui9"}
        )

        expected_data = {
            'user': {
                'login': 'jcui9',
                'name': 'jcui9',
                'id': 'MDQ6VXNlcjE1MTU1',
                'email': 'jcui9@ncsu.edu',
                'createdAt': '2019-09-11T17:08:06Z'
            }
        }
        assert response == expected_data


