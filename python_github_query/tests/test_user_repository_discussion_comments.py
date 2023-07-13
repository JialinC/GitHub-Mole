import pytest
from python_github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments


@pytest.mark.usefixtures("graphql_client")
class TestUserRepositoryDiscussionComments:
    def test_user_repository_discussion_comments_public(self):
        expected_data = {
            'user': {
                'login': 'JialinC',
                'repositoryDiscussionComments': {
                    'totalCount': 0,
                    'nodes': [],
                    'pageInfo': {
                        'endCursor': None,
                        'hasNextPage': False
                    }
                }
            }
        }
        count = 0
        for response in self.client.execute(query=UserRepositoryDiscussionComments(),
                                            substitutions={"user": "JialinC", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_repository_discussion_comments_enterprise(self):
        expected_data = {
            'user': {
                'login': 'jcui9',
                'repositoryDiscussionComments': {
                    'totalCount': 0,
                    'nodes': [],
                    'pageInfo': {
                        'endCursor': None,
                        'hasNextPage': False
                    }
                }
            }
        }
        count = 0
        for response in self.enterprise_client.execute(query=UserRepositoryDiscussionComments(),
                                                       substitutions={"user": "jcui9", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1


