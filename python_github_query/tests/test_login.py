import os
import pytest
from ..github_graphql.authentication import PersonalAccessTokenAuthenticator
from ..github_graphql.client import Client
from ..queries.login import UserLoginViewer, UserLogin


@pytest.fixture(scope="class")
def graphql_client():
    # Set up the GraphQL client
    client = Client(
        host="api.github.com", is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
    )

    enterprise_client = Client(
        host="github.ncsu.edu", is_enterprise=True,
        authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
    )
    yield [client, enterprise_client]


@pytest.mark.usefixtures("graphql_client")
class TestUserLogin:
    def test_user_login_viewer(self, graphql_client):
        client = graphql_client[0]
        response = client.execute(
            query=UserLoginViewer.query, substitutions={}
        )

        expected_data = {
            'viewer': {
                'login': 'JialinC'
            }
        }
        assert response == expected_data