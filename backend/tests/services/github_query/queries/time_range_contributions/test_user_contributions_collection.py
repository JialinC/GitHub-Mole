import re
from backend.app.services.github_query.queries.time_range_contributions.user_contributions_collection import UserContributionsCollection

class TestUserContributionsCollection:
    def test_user_contributions_collection_query_structure(self):
        # Instantiate the query class
        contributions_query = UserContributionsCollection()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(contributions_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                contributionsCollection(from: $start, to: $end) {
                    startedAt
                    endedAt
                    restrictedContributionsCount
                    totalCommitContributions
                    totalIssueContributions
                    totalPullRequestContributions
                    totalPullRequestReviewContributions
                    totalRepositoryContributions
                }
            }
        }
        '''.strip()
        # Remove all newlines
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The UserContributionsCollection query does not match the expected structure."

    def test_user_contributions_collection_processing(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "contributionsCollection": {
                    "startedAt": "2020-01-01T00:00:00Z",
                    "endedAt": "2020-12-31T23:59:59Z",
                    "restrictedContributionsCount": 5,
                    "totalCommitContributions": 150,
                    "totalIssueContributions": 45,
                    "totalPullRequestContributions": 30,
                    "totalPullRequestReviewContributions": 20,
                    "totalRepositoryContributions": 10,
                }
            }
        }

        # Expected processed data structure
        expected_contributions = {
            "res_con": 5,
            "commit": 150,
            "issue": 45,
            "pr": 30,
            "pr_review": 20,
            "repository": 10,
        }
        
        # Call the user_contributions_collection method and assert it returns the expected result
        processed_contributions = UserContributionsCollection.user_contributions_collection(raw_data)
        assert processed_contributions == expected_contributions, "Processed user contributions do not match the expected structure."
