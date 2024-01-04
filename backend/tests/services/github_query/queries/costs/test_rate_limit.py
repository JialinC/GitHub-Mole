import re
from backend.app.services.github_query.queries.costs.rate_limit import RateLimit

class TestRateLimitQuery:
    def test_rate_limit_query_structure(self):
        # Instantiate the RateLimit class
        rate_limit_query = RateLimit()
        # Convert the generated query to a string or the appropriate format
        query_string = str(rate_limit_query)
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            rateLimit(dryRun: $dryrun) {
                cost
                limit
                remaining
                resetAt
                used
            }
        }
        '''.strip()
        # Remove all newlines
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The RateLimit query does not match the expected structure."