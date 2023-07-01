import pytest
from python_github_query.queries.contributions import UserContributions


@pytest.mark.usefixtures("graphql_client")
class TestContributions:
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
        for response in self.client.execute(query=UserContributions(),
                                            substitutions={"user": "JialinC", "pg_size": 2,
                                                           "contribution_type": "pullRequests"}):
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
        for response in self.enterprise_client.execute(query=UserContributions(),
                                                       substitutions={"user": "jcui9", "pg_size": 2,
                                                                      "contribution_type": "pullRequests"}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_issues_public(self):
        expected_data = {'user': {
            'login': 'JialinC',
            'issues': {
                'totalCount': 17,
                'nodes': [{'createdAt': '2020-10-10T20:10:36Z'}, {'createdAt': '2020-10-11T01:04:19Z'}],
                'pageInfo': {'endCursor': 'Y3Vyc29yOnYyOpHOKtb-6g==', 'hasNextPage': True}}}}

        count = 0
        for response in self.client.execute(query=UserContributions(),
                                            substitutions={"user": "JialinC", "pg_size": 2,
                                                           "contribution_type": "issues"}):
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
        for response in self.enterprise_client.execute(query=UserContributions(),
                                                       substitutions={"user": "jcui9", "pg_size": 2,
                                                                      "contribution_type": "issues"}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_gists_public(self):
        expected_data = {'user': {
            'login': 'JialinC',
            'gists': {
                'totalCount': 0,
                'nodes': [],
                'pageInfo': {'endCursor': None, 'hasNextPage': False}}}}
        count = 0
        for response in self.client.execute(query=UserContributions(),
                                            substitutions={"user": "JialinC", "pg_size": 2,
                                                           "contribution_type": "gists"}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_gists_enterprise(self):
        expected_data = {'user': {
            'login': 'jcui9',
            'gists': {
                'totalCount': 0,
                'nodes': [],
                'pageInfo': {'endCursor': None, 'hasNextPage': False}}}}
        count = 0
        for response in self.enterprise_client.execute(query=UserContributions(),
                                                       substitutions={"user": "jcui9", "pg_size": 2,
                                                                      "contribution_type": "gists"}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_repository_discussion_public(self):
        expected_data = {'user': {
            'login': 'JialinC',
            'repositoryDiscussions': {
                'totalCount': 0,
                'nodes': [],
                'pageInfo': {'endCursor': None, 'hasNextPage': False}}}}
        count = 0
        for response in self.client.execute(query=UserContributions(),
                                            substitutions={"user": "JialinC", "pg_size": 2,
                                                           "contribution_type": "repositoryDiscussions"}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1

    def test_user_repository_discussion_enterprise(self):
        expected_data = {'user': {
            'login': 'jcui9',
            'repositoryDiscussions': {
                'totalCount': 0,
                'nodes': [],
                'pageInfo': {'endCursor': None, 'hasNextPage': False}}}}
        count = 0
        for response in self.enterprise_client.execute(query=UserContributions(),
                                                       substitutions={"user": "jcui9", "pg_size": 2,
                                                                      "contribution_type": "repositoryDiscussions"}):
            if count == 0:
                assert response == expected_data
            else:
                break
            count += 1
