import re
from backend.app.services.github_query.queries.contributions.user_issues import UserIssues

class TestUserIssues:
    def test_user_issues_query_structure(self):
        # Instantiate the UserIssues class
        user_issues_query = UserIssues()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(user_issues_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                login
                issues(first: $pg_size) {
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
        assert query_string == expected_query, "The UserIssues query does not match the expected structure."

    def test_user_issues_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "issues": {
                    "nodes": [
                        {"createdAt": "2021-01-01T00:00:00Z"},
                        {"createdAt": "2021-01-02T00:00:00Z"}
                    ]
                }
            }
        }
        
        expected_issues = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2021-01-02T00:00:00Z"}
        ]
        
        # Call the user_issues method and assert it returns the expected result
        issues = UserIssues.user_issues(raw_data)
        assert issues == expected_issues, "The processed issues do not match the expected structure."

    def test_created_before_time_method(self):
        issues = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2022-01-01T00:00:00Z"}
        ]
        time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
        # Call the created_before_time method and assert it returns the expected count
        count = UserIssues.created_before_time(issues, time)
        assert count == 1, "There should be 1 issue created before 2022."
