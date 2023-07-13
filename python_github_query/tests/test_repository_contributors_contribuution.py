import pytest
from python_github_query.queries.repositories.repository_contributors_contribution import RepositoryContributorsContribution


@pytest.mark.usefixtures("graphql_client")
class TestRepositoryContributorsContribution:
    def test_repository_contributors_contribution_public(self):
        response = self.client.execute(
            query=RepositoryContributorsContribution(), substitutions={"owner": "JialinC", "repo_name": "se-hw2",
                                                                       "id": { "id": "MDQ6VXNlcjM4NTQ5Njg5"}}
        )

        expected_data = {'repository': {'defaultBranchRef': {'target': {'history': {'totalCount': 4, 'nodes': [
            {'authoredDate': '2020-09-02T22:10:00Z', 'changedFilesIfAvailable': 22, 'additions': 2444, 'deletions': 48,
             'parents': {'totalCount': 2}},
            {'authoredDate': '2020-09-02T16:51:16Z', 'changedFilesIfAvailable': 22, 'additions': 424, 'deletions': 28,
             'parents': {'totalCount': 2}},
            {'authoredDate': '2020-08-26T03:44:12Z', 'changedFilesIfAvailable': 0, 'additions': 0, 'deletions': 0,
             'parents': {'totalCount': 2}},
            {'authoredDate': '2020-08-25T00:05:02Z', 'changedFilesIfAvailable': 15, 'additions': 414, 'deletions': 6,
             'parents': {'totalCount': 2}}]}}}}}

        assert response == expected_data

    def test_repository_contributors_contribution_enterprise(self):
        response = self.enterprise_client.execute(
            query=RepositoryContributorsContribution(), substitutions={"owner": "jcui9", "repo_name": "pyqt_UI",
                                                                       "id": {"id": "MDQ6VXNlcjE1MTU1"}}
        )

        expected_data = {'repository': {'defaultBranchRef': {'target': {'history': {'totalCount': 2, 'nodes': [
            {'authoredDate': '2023-07-05T18:34:36Z', 'changedFilesIfAvailable': 28, 'additions': 1892, 'deletions': 0,
             'parents': {'totalCount': 2}},
            {'authoredDate': '2023-04-01T02:50:07Z', 'changedFilesIfAvailable': 1, 'additions': 103, 'deletions': 0,
             'parents': {'totalCount': 1}}]}}}}}

        assert response == expected_data
