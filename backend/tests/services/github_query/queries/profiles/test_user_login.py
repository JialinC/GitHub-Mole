import re
from backend.app.services.github_query.queries.profiles.user_login import UserLoginViewer, UserLogin

class TestQueryGeneration:
    def test_user_login_viewer_query_structure(self):
        # Instantiate the UserLoginViewer class
        user_login_viewer_query = UserLoginViewer()
        query_string = str(user_login_viewer_query)
        # Define what the expected query should look like
        expected_query = '''
        query {
            viewer {
                login
            }
        }
        '''.strip()
        # Remove all newlines
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The UserLoginViewer query does not match the expected structure."

    def test_user_login_query_structure(self):
        # Instantiate the UserLogin class
        user_login_query = UserLogin()
        
        # Substitute the "$user" argument with a test value and convert to string
        query_string = user_login_query.substitute(user="testuser").__str__()
        # Define what the expected query should look like with the substituted value
        expected_query = '''
        query {
            user(login: "$user") {
                login
                name
                id
                email
                createdAt
            }
        }
        '''.replace("$user", "testuser").strip()  # Replace the placeholder and remove any leading/trailing whitespace
        # Remove all newlines
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The UserLogin query does not match the expected structure."

