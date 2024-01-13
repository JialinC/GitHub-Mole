import re
from backend.app.services.github_query.queries.contributions.user_repositories import UserRepositories

class TestUserRepositories:
    def test_user_repositories_query_structure(self):
        # Instantiate the UserGists class
        user_repositories_query = UserRepositories()
        # Convert the generated query to a string or the appropriate format
        query_string = str(user_repositories_query)
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                repositories(first: $pg_size, isFork: $is_fork, ownerAffiliations: $ownership, orderBy: $order_by) {
                    totalCount
                    nodes {
                        name
                        isEmpty
                        createdAt
                        updatedAt
                        forkCount
                        stargazerCount
                        watchers {
                            totalCount
                        }
                        primaryLanguage {
                            name
                        }
                        languages(first: 100, orderBy: {field: SIZE, direction: DESC}) {
                            totalSize
                            edges {
                                size
                                node {
                                    name
                                }
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
        '''.strip()  # Use .strip() to remove any leading/trailing whitespace
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The UserRepositories query does not match the expected structure."

    def test_user_repositories_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "repositories": {
                    "nodes": [
                        {
                            "name": "Repo1",
                            "isEmpty": False,
                            "createdAt": "2020-01-01T00:00:00Z",
                            "updatedAt": "2021-01-01T00:00:00Z",
                            "forkCount": 5,
                            "stargazerCount": 10,
                            "watchers": {"totalCount": 3},
                            "primaryLanguage": {"name": "Python"},
                            "languages": {
                                "totalSize": 1000,
                                "edges": [
                                    {"size": 600, "node": {"name": "Python"}},
                                    {"size": 400, "node": {"name": "JavaScript"}}
                                ]
                            }
                        },
                        {
                            "name": "Repo2",
                            "isEmpty": True,
                            "createdAt": "2021-01-01T00:00:00Z",
                            "updatedAt": "2022-01-01T00:00:00Z",
                            "forkCount": 2,
                            "stargazerCount": 5,
                            "watchers": {"totalCount": 1},
                            "primaryLanguage": {"name": "JavaScript"},
                            "languages": {
                                "totalSize": 500,
                                "edges": [
                                    {"size": 500, "node": {"name": "JavaScript"}}
                                ]
                            }
                        }
                    ]
                }
            }
        }
        expected_repositories = [
            {
                "name": "Repo1",
                "isEmpty": False,
                "createdAt": "2020-01-01T00:00:00Z",
                "updatedAt": "2021-01-01T00:00:00Z",
                "forkCount": 5,
                "stargazerCount": 10,
                "watchers": {"totalCount": 3},
                "primaryLanguage": {"name": "Python"},
                "languages": {
                    "totalSize": 1000,
                    "edges": [
                        {"size": 600, "node": {"name": "Python"}},
                        {"size": 400, "node": {"name": "JavaScript"}}
                    ]
                }
            },
            {
                "name": "Repo2",
                "isEmpty": True,
                "createdAt": "2021-01-01T00:00:00Z",
                "updatedAt": "2022-01-01T00:00:00Z",
                "forkCount": 2,
                "stargazerCount": 5,
                "watchers": {"totalCount": 1},
                "primaryLanguage": {"name": "JavaScript"},
                "languages": {
                    "totalSize": 500,
                    "edges": [
                        {"size": 500, "node": {"name": "JavaScript"}}
                    ]
                }
            }
        ]
        repositories = UserRepositories.user_repositories(raw_data)
        assert repositories == expected_repositories, "The processed repositories do not match the expected structure."

    def test_cumulated_repository_stats_method_before(self):
        repo_list = [
            {
                "name": "Repo1",
                "createdAt": "2020-01-01T00:00:00Z",
                "forkCount": 5,
                "stargazerCount": 10,
                "watchers": {"totalCount": 3},
                "languages": {
                    "totalSize": 1000,
                    "edges": [
                        {"size": 600, "node": {"name": "Python"}},
                        {"size": 400, "node": {"name": "JavaScript"}}
                    ]
                }
            }
        ]
        repo_stats = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0, "total_size": 0}
        lang_stats = {}
        end = "2022-01-01T00:00:00Z"
        UserRepositories.cumulated_repository_stats(repo_list, repo_stats, lang_stats, end, None, 'before')

        assert repo_stats["total_count"] == 1, "Total count of repositories should be 1."
        assert repo_stats["fork_count"] == 5, "Fork count should be 5."
        assert repo_stats["stargazer_count"] == 10, "Stargazer count should be 10."
        assert lang_stats["Python"] == 600, "Python size should be 600."
        assert lang_stats["JavaScript"] == 400, "JavaScript size should be 400."

    def test_cumulated_repository_stats_method_after(self):
        repo_list = [
            {
                "name": "Repo1",
                "createdAt": "2020-01-01T00:00:00Z",
                "forkCount": 5,
                "stargazerCount": 10,
                "watchers": {"totalCount": 3},
                "languages": {
                    "totalSize": 1000,
                    "edges": [
                        {"size": 600, "node": {"name": "Python"}},
                        {"size": 400, "node": {"name": "JavaScript"}}
                    ]
                }
            }
        ]
        repo_stats = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0, "total_size": 0}
        lang_stats = {}
        end = "2019-01-01T00:00:00Z"
        UserRepositories.cumulated_repository_stats(repo_list, repo_stats, lang_stats, end, None, 'after')

        assert repo_stats["total_count"] == 1, "Total count of repositories should be 1."
        assert repo_stats["fork_count"] == 5, "Fork count should be 5."
        assert repo_stats["stargazer_count"] == 10, "Stargazer count should be 10."
        assert lang_stats["Python"] == 600, "Python size should be 600."
        assert lang_stats["JavaScript"] == 400, "JavaScript size should be 400."

    def test_cumulated_repository_stats_method_between(self):
        repo_list = [
            {
                "name": "Repo1",
                "createdAt": "2020-01-01T00:00:00Z",
                "forkCount": 5,
                "stargazerCount": 10,
                "watchers": {"totalCount": 3},
                "languages": {
                    "totalSize": 1000,
                    "edges": [
                        {"size": 600, "node": {"name": "Python"}},
                        {"size": 400, "node": {"name": "JavaScript"}}
                    ]
                }
            }
        ]
        repo_stats = {"total_count": 0, "fork_count": 0, "stargazer_count": 0, "watchers_count": 0, "total_size": 0}
        lang_stats = {}
        start = "2019-01-01T00:00:00Z"
        end = "2021-01-01T00:00:00Z"
        UserRepositories.cumulated_repository_stats(repo_list, repo_stats, lang_stats, start, end, 'between')

        assert repo_stats["total_count"] == 1, "Total count of repositories should be 1."
        assert repo_stats["fork_count"] == 5, "Fork count should be 5."
        assert repo_stats["stargazer_count"] == 10, "Stargazer count should be 10."
        assert lang_stats["Python"] == 600, "Python size should be 600."
        assert lang_stats["JavaScript"] == 400, "JavaScript size should be 400."
