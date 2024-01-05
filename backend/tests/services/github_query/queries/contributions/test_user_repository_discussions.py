import re
from backend.app.services.github_query.queries.contributions.user_repository_discussions import UserRepositoryDiscussions

class TestUserRepositoryDiscussions:
    def test_user_repository_discussions_query_structure(self):
        # Instantiate the UserRepositoryDiscussions class
        user_repository_discussions_query = UserRepositoryDiscussions()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(user_repository_discussions_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                login
                repositoryDiscussions(first: $pg_size) {
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
        assert query_string == expected_query, "The UserRepositoryDiscussions query does not match the expected structure."

    def test_user_repository_discussions_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "repositoryDiscussions": {
                    "nodes": [
                        {"createdAt": "2021-01-01T00:00:00Z"},
                        {"createdAt": "2021-01-02T00:00:00Z"}
                    ]
                }
            }
        }
        
        expected_discussions = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2021-01-02T00:00:00Z"}
        ]
        
        # Call the user_repository_discussions method and assert it returns the expected result
        repository_discussions = UserRepositoryDiscussions.user_repository_discussions(raw_data)
        assert repository_discussions == expected_discussions, "The processed repository discussions do not match the expected structure."

    def test_created_before_time_method(self):
        # Example repository discussions and a comparison time
        repository_discussions = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2022-01-01T00:00:00Z"}
        ]
        time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
        # Call the created_before_time method and assert it returns the expected count
        count = UserRepositoryDiscussions.created_before_time(repository_discussions, time)
        assert count == 1, "There should be 1 discussion created before 2022."
