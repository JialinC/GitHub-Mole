import pytest
from github_query.queries.utils.rate_limit import RateLimit


@pytest.mark.usefixtures("graphql_client")
class TestRateLimit:
    def test_rate_limit_public(self):
        response = self.client.execute(query=RateLimit(), substitutions={"dryrun": True})
        assert response['rateLimit']['cost'] == 1
        assert response['rateLimit']['limit'] == 5000

    def test_user_gists_enterprise(self):
        response = self.enterprise_client.execute(query=RateLimit(), substitutions={"dryrun": True})
        assert response['rateLimit']['cost'] == 1
        assert response['rateLimit']['limit'] == 200
