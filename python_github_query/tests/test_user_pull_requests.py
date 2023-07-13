import pytest
from python_github_query.queries.contributions.user_pull_requests import UserPullRequests


@pytest.mark.usefixtures("graphql_client")
class TestUserPullRequests:
    def test_user_pull_request_public(self):
        expected_data1 = {'user': {
            'login': 'JialinC',
            'pullRequests': {
                'totalCount': 37,
                'nodes': [{'createdAt': '2020-08-08T14:56:14Z'}, {'createdAt': '2020-08-13T02:27:59Z'}],
                'pageInfo': {'endCursor': 'Y3Vyc29yOnYyOpHOG9eBZw==', 'hasNextPage': True}}}}
        expected_data2 = {'user': {
            'login': 'JialinC',
            'pullRequests': {
                'totalCount': 37,
                'nodes': [{'createdAt': '2020-08-18T04:24:35Z'}, {'createdAt': '2020-08-25T00:04:53Z'}],
                'pageInfo': {'endCursor': 'Y3Vyc29yOnYyOpHOHC8VFw==', 'hasNextPage': True}}}}
        count = 0
        for response in self.client.execute(query=UserPullRequests(),
                                            substitutions={"user": "JialinC", "pg_size": 2}):
            if count == 0:
                assert response == expected_data1
            elif count == 1:
                assert response == expected_data2
            else:
                break
            count += 1

    def test_user_pull_request_enterprise(self):
        expected_data = {'user': {
            'login': 'jcui9',
            'pullRequests': {
                'totalCount': 2,
                'nodes': [{'createdAt': '2023-04-04T15:31:47Z'}, {'createdAt': '2023-04-04T18:12:30Z'}],
                'pageInfo': {'endCursor': 'Y3Vyc29yOnYyOpHOAAGKIQ==', 'hasNextPage': False}}}}

        count = 0
        for response in self.enterprise_client.execute(query=UserPullRequests(),
                                                       substitutions={"user": "jcui9", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1
