import re
from backend.app.services.github_query.queries.repositories.repository_contributors import RepositoryContributors


class TestRepositoryContributors:
    def test_repository_contributors_query_structure(self):
        # Instantiate the RepositoryContributors class
        repo_contributors_query = RepositoryContributors()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(repo_contributors_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            repository(owner: "$owner", name: "$repo_name") {
                defaultBranchRef {
                    target {
                        ... on Commit {
                            history(first: $pg_size) {
                                totalCount
                                nodes {
                                    author {
                                        name
                                        email
                                        user {
                                            login
                                        }
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
        assert query_string == expected_query, "The RepositoryContributors query does not match the expected structure."

    def test_extract_unique_author_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "repository": {
                "defaultBranchRef": {
                    "target": {
                        "history": {
                            "nodes": [
                                {
                                    "author": {
                                        "name": "Alice",
                                        "user": {"login": "aliceGit"}
                                    }
                                },
                                {
                                    "author": {
                                        "name": "Bob",
                                        "user": {"login": "bobGit"}
                                    }
                                },
                                # Assuming a commit with no associated user
                                {
                                    "author": {
                                        "name": "Charlie",
                                        "user": None
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
        
        unique_authors = RepositoryContributors.extract_unique_author(raw_data)
        
        expected_unique_authors = {
            'name': {'Alice', 'Bob', 'Charlie'},
            'login': {'aliceGit', 'bobGit'}
        }

        # Assert that the processed unique authors match the expected structure
        assert unique_authors == expected_unique_authors, "The processed unique authors do not match the expected structure."
