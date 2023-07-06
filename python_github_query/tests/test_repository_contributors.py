import pytest
from python_github_query.queries.repository_contributors import RepositoryContributors


@pytest.mark.usefixtures("graphql_client")
class TestRepositoryContributors:
    def test_repository_contributors_public(self):
        response = self.client.execute(
            query=RepositoryContributors(), substitutions={"owner": "JialinC", "repo_name": "se-hw2"}
        )

        expected_data = {'repository': {'defaultBranchRef': {'target': {'history': {
            'nodes': [{'author': {'user': None}}, {'author': {'user': None}},
                      {'author': {'user': {'login': 'JialinC'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': None}},
                      {'author': {'user': {'login': 'JialinC'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'ericbibiwang'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'ericbibiwang'}}},
                      {'author': {'user': {'login': 'wangdavid84'}}}, {'author': {'user': {'login': 'wangdavid84'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'wangdavid84'}}}, {'author': {'user': None}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'JialinC'}}},
                      {'author': {'user': {'login': 'wangdavid84'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': None}}, {'author': {'user': None}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': None}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'JialinC'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': None}},
                      {'author': {'user': {'login': 'wangdavid84'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': {'login': 'yrahul3910'}}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'yrahul3910'}}},
                      {'author': {'user': None}}, {'author': {'user': None}},
                      {'author': {'user': {'login': 'yrahul3910'}}}]}}}}}

        assert response == expected_data

    def test_repository_contributors_enterprise(self):
        response = self.enterprise_client.execute(
            query=RepositoryContributors(), substitutions={"owner": "jcui9", "repo_name": "pyqt_UI"}
        )

        expected_data = {'repository': {'defaultBranchRef': {'target': {'history': {
            'nodes': [{'author': {'user': {'login': 'jcui9'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': None}}, {'author': {'user': None}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'anguyen9'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'anguyen9'}}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'anguyen9'}}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'anguyen9'}}},
                      {'author': {'user': None}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'jdjohns4'}}},
                      {'author': {'user': {'login': 'jdjohns4'}}}, {'author': {'user': {'login': 'anguyen9'}}},
                      {'author': {'user': {'login': 'jcui9'}}}, {'author': {'user': None}}]}}}}}

        assert response == expected_data



