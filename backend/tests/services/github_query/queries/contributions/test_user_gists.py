import re
from backend.app.services.github_query.queries.contributions.user_gists import UserGists

class TestUserGists:
    def test_user_gists_query_structure(self):
        # Instantiate the UserGists class
        user_gists_query = UserGists()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(user_gists_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                login
                gists(first: $pg_size) {
                    totalCount
                    nodes {
                        createdAt
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        '''.strip()  # Use .strip() to remove any leading/trailing whitespace
        # Remove all newlines
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The UserGists query does not match the expected structure."

    def test_user_gists_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "gists": {
                    "nodes": [
                        {"createdAt": "2021-01-01T00:00:00Z"},
                        {"createdAt": "2021-01-02T00:00:00Z"}
                    ]
                }
            }
        }
        
        expected_gists = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2021-01-02T00:00:00Z"}
        ]
        
        # Call the user_gists method and assert it returns the expected result
        gists = UserGists.user_gists(raw_data)
        assert gists == expected_gists, "The processed gists do not match the expected structure."


    def test_created_before_time_method(self):
        gists = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2022-01-01T00:00:00Z"}
        ]
        time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
        # Call the created_before_time method and assert it returns the expected count
        count = UserGists.created_before_time(gists, time)
        assert count == 1, "There should be 1 gist created before 2022."

