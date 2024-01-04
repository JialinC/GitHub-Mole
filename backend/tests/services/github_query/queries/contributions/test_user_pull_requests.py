import re
from backend.app.services.github_query.queries.contributions.user_pull_requests import UserPullRequests

class TestUserPullRequests:
    def test_user_pull_requests_query_structure(self):
        # Instantiate the UserPullRequests class
        user_pull_requests_query = UserPullRequests()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(user_pull_requests_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                login
                pullRequests(first: $pg_size) {
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
        assert query_string == expected_query, "The UserPullRequests query does not match the expected structure."

    def test_user_pull_requests_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "pullRequests": {
                    "nodes": [
                        {"createdAt": "2021-01-01T00:00:00Z"},
                        {"createdAt": "2021-01-02T00:00:00Z"}
                    ]
                }
            }
        }
        
        expected_pull_requests = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2021-01-02T00:00:00Z"}
        ]
        
        # Call the user_pull_requests method and assert it returns the expected result
        pull_requests = UserPullRequests.user_pull_requests(raw_data)
        assert pull_requests == expected_pull_requests, "The processed pull requests do not match the expected structure."

    def test_created_before_time_method(self):
        pull_requests = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2022-01-01T00:00:00Z"}
        ]
        time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
        # Call the created_before_time method and assert it returns the expected count
        count = UserPullRequests.created_before_time(pull_requests, time)
        assert count == 1, "There should be 1 pull request created before 2022."
