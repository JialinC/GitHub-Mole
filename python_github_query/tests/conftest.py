import os
import pytest
from python_github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from python_github_query.github_graphql.client import Client


@pytest.fixture(scope="module")
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