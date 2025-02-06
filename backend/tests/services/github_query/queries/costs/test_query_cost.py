import re
from backend.app.services.github_query.queries.costs.query_cost import QueryCost
from backend.app.services.github_query.github_graphql.query import Query

class TestQueryCost:
    def test_query_cost_structure(self):
        # Simulate a test query node that might be passed into QueryCost
        test_query_node = Query(
            "testQuery",
            fields=["field1", "field2"]
        )

        # Instantiate the QueryCost class with the test query node
        query_cost = QueryCost(test_query_node)
        # Convert the generated query to a string or the appropriate format
        query_string = str(query_cost)
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            testQuery {
                field1
                field2
            }
            rateLimit(dryRun: $dryrun) {
                cost
                remaining
                resetAt
            }
        }
        '''.strip()  # Use .strip() to remove any leading/trailing whitespace
        # Remove all newlines
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The QueryCost does not match the expected structure."
        
