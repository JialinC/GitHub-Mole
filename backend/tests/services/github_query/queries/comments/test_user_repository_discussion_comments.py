import re
from backend.app.services.github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments

class TestUserRepositoryDiscussionComments:
    def test_user_repository_discussion_comments_query_structure(self):
        # Instantiate the UserRepositoryDiscussionComments class
        user_repository_discussion_comments_query = UserRepositoryDiscussionComments()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(user_repository_discussion_comments_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                login
                repositoryDiscussionComments(first: $pg_size) {
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
        assert query_string == expected_query, "The UserRepositoryDiscussionComments query does not match the expected structure."

    def test_user_repository_discussion_comments_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "repositoryDiscussionComments": {
                    "nodes": [
                        {"createdAt": "2021-01-01T00:00:00Z"},
                        {"createdAt": "2021-01-02T00:00:00Z"}
                    ]
                }
            }
        }
        
        expected_comments = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2021-01-02T00:00:00Z"}
        ]
        
        # Call the user_gist_comments method and assert it returns the expected result
        repository_discussion_comments = UserRepositoryDiscussionComments.user_repository_discussion_comments(raw_data)
        assert repository_discussion_comments == expected_comments, "The processed repository discussion comments comments do not match the expected structure."


    def test_created_before_time_method(self):
        user_repository_discussion_comments = [
            {"createdAt": "2021-01-01T00:00:00Z"},
            {"createdAt": "2022-01-01T00:00:00Z"}
        ]
        time = "2022-01-01T00:00:00Z"  # Set a time for comparison
        
        # Call the created_before_time method and assert it returns the expected count
        count = UserRepositoryDiscussionComments.created_before_time(user_repository_discussion_comments, time)
        assert count == 1, "There should be 1 comment created before 2022."