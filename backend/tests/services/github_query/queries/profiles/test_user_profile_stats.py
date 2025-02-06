import re
from backend.app.services.github_query.queries.profiles.user_profile_stats import UserProfileStats

class TestUserProfileStats:
    def test_user_profile_stats_query_structure(self):
        user_profile_stats_query = UserProfileStats()
        
        # Convert the generated query to a string or the appropriate format
        query_string = str(user_profile_stats_query)
        
        # Define what the expected query should look like, including all fields
        expected_query = '''
        query {
            user(login: "$user") {
                login
                name
                email
                createdAt
                bio
                company
                isBountyHunter
                isCampusExpert
                isDeveloperProgramMember
                isEmployee
                isGitHubStar
                isHireable
                isSiteAdmin
                watching {
                    totalCount
                }
                starredRepositories {
                    totalCount
                }
                following {
                    totalCount
                }
                followers {
                    totalCount
                }
                gists {
                    totalCount
                }
                issues {
                    totalCount
                }
                projects {
                    totalCount
                }
                pullRequests {
                    totalCount
                }
                repositories {
                    totalCount
                }
                repositoryDiscussions {
                    totalCount
                }
                gistComments {
                    totalCount
                }
                issueComments {
                    totalCount
                }
                commitComments {
                    totalCount
                }
                repositoryDiscussionComments {
                    totalCount
                }
            }
        }
        '''.strip()
        # Remove all newlines
        expected_query = expected_query.replace("\n", "")
        # Remove extra spaces using regex
        expected_query = re.sub(' +', ' ', expected_query)
        # Assert that the generated query matches the expected query
        assert query_string == expected_query, "The UserProfileStats query does not match the expected structure."

    
    def test_profile_stats_method(self):
        # Simulated raw data returned by the query
        raw_data = {
            "user": {
                "login": "test_user",
                "createdAt": "2021-01-01T00:00:00Z",
                "company": "TestCompany",
                "bio": "This is a bio.",
                "isBountyHunter": False,
                "isCampusExpert": False,
                "isDeveloperProgramMember": False,
                "isEmployee": False,
                "isGitHubStar": False,
                "isHireable": True,
                "isSiteAdmin": False,
                "followers": {"totalCount": 100},
                "gists": {"totalCount": 5},
                "issues": {"totalCount": 10},
                "projects": {"totalCount": 3},
                "pullRequests": {"totalCount": 7},
                "repositories": {"totalCount": 12},
                "repositoryDiscussions": {"totalCount": 1},
                "gistComments": {"totalCount": 4},
                "issueComments": {"totalCount": 8},
                "commitComments": {"totalCount": 6},
                "repositoryDiscussionComments": {"totalCount": 2},
                "watching": {"totalCount": 20},
                "starredRepositories": {"totalCount": 15},
                "following": {"totalCount": 25}
            }
        }
        
        expected_profile_stats = {
            "github": "test_user",
            "created_at": "2021-01-01T00:00:00Z",
            "company": "TestCompany",
            "followers": 100,
            "gists": 5,
            "issues": 10,
            "projects": 3,
            "pull_requests": 7,
            "repositories": 12,
            "repository_discussions": 1,
            "gist_comments": 4,
            "issue_comments": 8,
            "commit_comments": 6,
            "repository_discussion_comments": 2,
            "watching": 20,
            "starred_repositories": 15,
            "following": 25,
            # ... add any additional fields as needed
        }
        
        # Call the profile_stats method and assert it returns the expected result
        profile_stats = UserProfileStats.profile_stats(raw_data)
        assert profile_stats == expected_profile_stats, "The processed profile stats do not match the expected structure."

