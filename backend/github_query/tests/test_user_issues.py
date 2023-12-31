import pytest
from github_query.queries.contributions.user_issues import UserIssues


@pytest.mark.usefixtures("graphql_client")
class TestUserIssues:
    def test_user_issues_public(self):
        expected_data = {'user': {
            'login': 'JialinC',
            'issues': {
                'totalCount': 17,
                'nodes': [{'createdAt': '2020-10-10T20:10:36Z'}, {'createdAt': '2020-10-11T01:04:19Z'}],
                'pageInfo': {'endCursor': 'Y3Vyc29yOnYyOpHOKtb-6g==', 'hasNextPage': True}}}}

        count = 0
        for response in self.client.execute(query=UserIssues(),
                                            substitutions={"user": "JialinC", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_issues_enterprise(self):
        expected_data = {'user': {
            'login': 'jcui9',
            'issues': {
                'totalCount': 5,
                'nodes': [{'createdAt': '2021-01-29T22:01:09Z'}, {'createdAt': '2021-01-29T22:08:13Z'}],
                'pageInfo': {'endCursor': 'Y3Vyc29yOnYyOpHOAAHU7g==', 'hasNextPage': True}}}}

        count = 0
        for response in self.enterprise_client.execute(query=UserIssues(),
                                                       substitutions={"user": "jcui9", "pg_size": 2}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1
