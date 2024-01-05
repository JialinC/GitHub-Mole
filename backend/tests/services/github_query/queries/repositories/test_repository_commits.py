import re
import pytest
from backend.app.services.github_query.queries.repositories.repository_commits import RepositoryCommits

class TestRepositoryCommits:
    def test_repository_commits_query_structure(self):
        # Instantiate the RepositoryCommits class
        repository_commits_query = RepositoryCommits()

        # Convert the generated query to a string or the appropriate format
        query_string = str(repository_commits_query)

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
                                    authoredDate
                                    changedFilesIfAvailable
                                    additions
                                    deletions
                                    message
                                    parents (first: 2) {
                                        totalCount
                                    }
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
        assert query_string == expected_query, "The RepositoryCommits query does not match the expected structure."

    
@pytest.fixture
def mock_raw_data_single_commit():
    return {
        "repository": {
            "defaultBranchRef": {
                "target": {
                    "history": {
                        "nodes": [
                            {
                                "authoredDate": "2021-01-01T00:00:00Z",
                                "changedFilesIfAvailable": 5,
                                "additions": 10,
                                "deletions": 4,
                                "message": "Initial commit",
                                "parents": {"totalCount": 1},
                                "author": {
                                    "name": "John Doe",
                                    "email": "john@example.com",
                                    "user": {"login": "john_doe"}
                                }
                            }
                        ]
                    }
                }
            }
        }
    }

@pytest.fixture
def mock_raw_data_multiple_commits_multiple_parents():
    return {
        "repository": {
            "defaultBranchRef": {
                "target": {
                    "history": {
                        "nodes": [
                            {
                                "authoredDate": "2021-01-01T00:00:00Z",
                                "changedFilesIfAvailable": 5,
                                "additions": 10,
                                "deletions": 4,
                                "message": "Initial commit",
                                "parents": {"totalCount": 1},
                                "author": {
                                    "name": "John Doe",
                                    "email": "john@example.com",
                                    "user": {"login": "john_doe"}
                                }
                            },
                            {
                                "authoredDate": "2021-01-01T00:00:00Z",
                                "changedFilesIfAvailable": 5,
                                "additions": 10,
                                "deletions": 4,
                                "message": "Initial commit",
                                "parents": {"totalCount": 6},
                                "author": {
                                    "name": "John Doe",
                                    "email": "john@example.com",
                                    "user": {"login": "john_doe"}
                                }
                            }
                        ]
                    }
                }
            }
        }
    }

@pytest.fixture
def mock_raw_data_multiple_commits():
    return {
        "repository": {
            "defaultBranchRef": {
                "target": {
                    "history": {
                        "nodes": [
                            {
                                "authoredDate": "2021-01-01T00:00:00Z",
                                "changedFilesIfAvailable": 3,
                                "additions": 7,
                                "deletions": 2,
                                "message": "First commit",
                                "parents": {"totalCount": 1},
                                "author": {
                                    "name": "",
                                    "email": "alice@example.com",
                                    "user": {"login": "alice_smith"}
                                }
                            },
                            {
                                "authoredDate": "2021-01-02T00:00:00Z",
                                "changedFilesIfAvailable": 6,
                                "additions": 15,
                                "deletions": 5,
                                "message": "Second commit",
                                "parents": {"totalCount": 1},
                                "author": {
                                    "name": "Bob Brown",
                                    "email": "bob@example.com",
                                    "user": {}
                                }
                            },
                            {
                                "authoredDate": "2021-01-03T00:00:00Z",
                                "changedFilesIfAvailable": 2,
                                "additions": 4,
                                "deletions": 1,
                                "message": "Third commit",
                                "parents": {"totalCount": 1},
                                "author": {
                                    "name": "Alice Smith",
                                    "email": "alice@example.com",
                                    "user": {"login": "alice_smith"}
                                }
                            }
                            # Add more commit nodes as needed to represent different scenarios
                        ]
                    }
                }
            }
        }
    }

class TestRepositoryCommits:
    def test_single_commit(self, mock_raw_data_single_commit):
        """Test with multiple commits."""
        result = RepositoryCommits.commits_list(mock_raw_data_single_commit)
        
        assert "John Doe" in result, "John Doe should be in the cumulative commits."
        assert result["John Doe"]["john_doe"]["total_additions"] == 10, "John Doe should have 10 additions."
        assert result["John Doe"]["john_doe"]["total_deletions"] == 4, "John Doe should have 4 deletions."
        assert result["John Doe"]["john_doe"]["total_files"] == 5, "John Doe should have 5 files."
        assert result["John Doe"]["john_doe"]["total_commits"] == 1, "John Doe should have 1 commits."

    def test_multiple_commits_multiple_parents(self, mock_raw_data_multiple_commits_multiple_parents):
        """Test with multiple commits."""
        result = RepositoryCommits.commits_list(mock_raw_data_multiple_commits_multiple_parents)

        assert "John Doe" in result, "John Doe should be in the cumulative commits."
        assert result["John Doe"]["john_doe"]["total_additions"] == 10, "John Doe should have 10 additions."
        assert result["John Doe"]["john_doe"]["total_deletions"] == 4, "John Doe should have 4 deletions."
        assert result["John Doe"]["john_doe"]["total_files"] == 5, "John Doe should have 5 files."
        assert result["John Doe"]["john_doe"]["total_commits"] == 1, "John Doe should have 1 commits."

    def test_multiple_commits(self, mock_raw_data_multiple_commits):
        """Test with multiple commits."""
        result = RepositoryCommits.commits_list(mock_raw_data_multiple_commits)
        {'': {'alice_smith': {'total_additions': 7, 'total_deletions': 2, 'total_files': 3, 'total_commits': 1}}, 
         'Bob Brown': {'total_additions': 15, 'total_deletions': 5, 'total_files': 6, 'total_commits': 1}, 
         'Alice Smith': {'alice_smith': {'total_additions': 4, 'total_deletions': 1, 'total_files': 2, 'total_commits': 1}}}
       
        assert "" in result, "empty string should be in the cumulative commits."
        assert result[""]["alice_smith"]["total_additions"] == 7, "alice_smith without name should have 7 additions."
        assert result["Bob Brown"]["total_deletions"] == 5, "Bob Brown without login should have 5 deletions."
        assert result["Alice Smith"]["alice_smith"]["total_files"] == 2, "Alice Smith with login should have 2 files."