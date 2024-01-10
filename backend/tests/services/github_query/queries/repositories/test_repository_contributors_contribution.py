import re
from backend.app.services.github_query.queries.repositories.repository_contributors_contribution import RepositoryContributorsContribution

class TestRepositoryContributorsContributionInit:
    def test_repository_contributors_contribution_query_structure(self):
        # Instantiate the RepositoryContributorsContribution class
        repository_contributors_contribution_query = RepositoryContributorsContribution()

        # Convert the generated query to a string or the appropriate format
        query_string = str(repository_contributors_contribution_query)

        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            repository(owner: "$owner", name: "$repo_name") {
                defaultBranchRef {
                    target {
                        ... on Commit {
                            history(author: $id, first: $pg_size) {
                                totalCount
                                nodes {
                                    authoredDate
                                    changedFilesIfAvailable
                                    additions
                                    deletions
                                    message
                                    parents (first: 2) {
                                        totalCount
                                    }
                                }
                                pageInfo {
                                    endCursor
                                    hasNextPage
                                }
                            }
                        }
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
        assert query_string == expected_query, "The RepositoryContributorsContribution query does not match the expected structure."

    # The test can be run using a Pytest command.
    def test_user_cumulated_contribution(self):
        # Simulated raw data returned by the query
        raw_data = {
            "repository": {
                "defaultBranchRef": {
                    "target": {
                        "history": {
                            "nodes": [
                                {"additions": 10, "deletions": 5, "parents": {"totalCount": 1}},
                                {"additions": 7, "deletions": 2, "parents": {"totalCount": 1}}
                            ]
                        }
                    }
                }
            }
        }
        
        # Expected cumulative contribution result
        expected_cumulative_contribution = {
            "total_additions": 17, 
            "total_deletions": 7, 
            "total_commits": 2
        }
        
        # Call the user_cumulated_contribution method and assert it returns the expected result
        cumulative_contribution = RepositoryContributorsContribution.user_cumulated_contribution(raw_data)
        assert cumulative_contribution == expected_cumulative_contribution, "The cumulated contributions do not match the expected structure."

    def test_user_commit_contribution(self):
        # Simulated raw data returned by the query
        raw_data = {
            "repository": {
                "defaultBranchRef": {
                    "target": {
                        "history": {
                            "nodes": [
                                {"authoredDate": "2021-01-01T00:00:00Z", "changedFilesIfAvailable": 3, "additions": 10, "deletions": 5, "message": "Initial commit", "parents": {"totalCount": 1}},
                                {"authoredDate": "2021-01-02T00:00:00Z", "changedFilesIfAvailable": 2, "additions": 7, "deletions": 2, "message": "Update README", "parents": {"totalCount": 1}}
                            ]
                        }
                    }
                }
            }
        }

        # Expected list of individual commit contributions
        expected_commit_contributions = [
            {"authoredDate": "2021-01-01T00:00:00Z", "changedFiles": 3, "additions": 10, "deletions": 5, "message": "Initial commit"},
            {"authoredDate": "2021-01-02T00:00:00Z", "changedFiles": 2, "additions": 7, "deletions": 2, "message": "Update README"}
        ]

        # Call the user_commit_contribution method and assert it returns the expected result
        commit_contributions = RepositoryContributorsContribution.user_commit_contribution(raw_data)
        assert commit_contributions == expected_commit_contributions, "The individual commit contributions do not match the expected structure."
