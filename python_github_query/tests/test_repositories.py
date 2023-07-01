import pytest
from python_github_query.queries.repositories import UserRepositories


@pytest.mark.usefixtures("graphql_client")
class TestRepositories:
    def test_user_repositories_public(self):
        fork_owner = {'user': {'repositories': {'nodes': [
            {'name': 'se20', 'isEmpty': False, 'createdAt': '2020-08-07T18:26:31Z', 'updatedAt': '2020-08-07T18:26:32Z',
             'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0}, 'primaryLanguage': {'name': 'Shell'},
             'languages': {'totalSize': 10243, 'totalCount': 1, 'edges': [{'size': 10243, 'node': {'name': 'Shell'}}]}},
            {'name': 'se20-1', 'isEmpty': False, 'createdAt': '2020-08-13T01:38:52Z',
             'updatedAt': '2020-08-27T14:15:22Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0},
             'primaryLanguage': {'name': 'Python'},
             'languages': {'totalSize': 678, 'totalCount': 1, 'edges': [{'size': 678, 'node': {'name': 'Python'}}]}},
            {'name': 'DrCCTProf', 'isEmpty': False, 'createdAt': '2020-08-15T18:07:38Z',
             'updatedAt': '2020-08-30T13:36:10Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0},
             'primaryLanguage': {'name': 'C++'}, 'languages': {'totalSize': 504009, 'totalCount': 5,
                                                               'edges': [{'size': 387670, 'node': {'name': 'C++'}},
                                                                         {'size': 72967, 'node': {'name': 'CMake'}},
                                                                         {'size': 39265, 'node': {'name': 'Shell'}},
                                                                         {'size': 3694, 'node': {'name': 'C'}},
                                                                         {'size': 413, 'node': {'name': 'Python'}}]}},
            {'name': 'se-hw2', 'isEmpty': False, 'createdAt': '2020-08-17T18:46:19Z',
             'updatedAt': '2020-09-02T22:48:35Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0},
             'primaryLanguage': {'name': 'Jupyter Notebook'}, 'languages': {'totalSize': 645653, 'totalCount': 7,
                                                                            'edges': [{'size': 627408, 'node': {
                                                                                'name': 'Jupyter Notebook'}},
                                                                                      {'size': 7939,
                                                                                       'node': {'name': 'JavaScript'}},
                                                                                      {'size': 4134,
                                                                                       'node': {'name': 'Go'}},
                                                                                      {'size': 2808,
                                                                                       'node': {'name': 'Rust'}},
                                                                                      {'size': 2420,
                                                                                       'node': {'name': 'Ruby'}},
                                                                                      {'size': 684,
                                                                                       'node': {'name': 'Dockerfile'}},
                                                                                      {'size': 260,
                                                                                       'node': {'name': 'Shell'}}]}},
            {'name': 'social-media-website', 'isEmpty': False, 'createdAt': '2020-09-07T02:30:23Z',
             'updatedAt': '2020-09-17T16:27:22Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0},
             'primaryLanguage': {'name': 'JavaScript'}, 'languages': {'totalSize': 51204, 'totalCount': 4, 'edges': [
                {'size': 45811, 'node': {'name': 'JavaScript'}}, {'size': 4142, 'node': {'name': 'Sass'}},
                {'size': 968, 'node': {'name': 'Dockerfile'}}, {'size': 283, 'node': {'name': 'HTML'}}]}}],
            'pageInfo': {
                'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMC0wOS0wNlQyMjozMDoyMy0wNDowMM4RfPlC',
                'hasNextPage': True}}}}
        fork_collaborator = {'user': {'repositories': {'nodes': [
            {'name': 'expertiza', 'isEmpty': False, 'createdAt': '2021-03-03T06:18:50Z',
             'updatedAt': '2021-03-25T02:15:52Z', 'forkCount': 1, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 2784658, 'totalCount': 9,
                                                                'edges': [{'size': 1933355, 'node': {'name': 'Ruby'}},
                                                                          {'size': 634348, 'node': {'name': 'HTML'}},
                                                                          {'size': 141740,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 54913, 'node': {'name': 'SCSS'}},
                                                                          {'size': 11046, 'node': {'name': 'Haml'}},
                                                                          {'size': 6533, 'node': {'name': 'Shell'}},
                                                                          {'size': 1308,
                                                                           'node': {'name': 'Dockerfile'}},
                                                                          {'size': 881, 'node': {'name': 'CSS'}},
                                                                          {'size': 534,
                                                                           'node': {'name': 'CoffeeScript'}}]}},
            {'name': 'LeetHub_Research', 'isEmpty': False, 'createdAt': '2022-01-21T09:26:22Z',
             'updatedAt': '2022-01-20T19:55:31Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0},
             'primaryLanguage': None, 'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}}], 'pageInfo': {
            'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMi0wMS0yMVQwNDoyNjoyMi0wNTowMM4a2QDX', 'hasNextPage': False}}}}
        not_fork_owner = {'user': {'repositories': {'nodes': [
            {'name': 'Multivariable-Calculus', 'isEmpty': False, 'createdAt': '2018-11-24T04:37:52Z',
             'updatedAt': '2023-05-06T06:31:47Z', 'forkCount': 4, 'stargazerCount': 5, 'watchers': {'totalCount': 0},
             'primaryLanguage': {'name': 'Jupyter Notebook'}, 'languages': {'totalSize': 4871884, 'totalCount': 1,
                                                                            'edges': [{'size': 4871884, 'node': {
                                                                                'name': 'Jupyter Notebook'}}]}},
            {'name': 'Kernel-PCA-Reconstruction-error-decision-boundary-algorithm', 'isEmpty': False,
             'createdAt': '2018-11-24T06:04:52Z', 'updatedAt': '2019-06-18T12:49:29Z', 'forkCount': 0,
             'stargazerCount': 1, 'watchers': {'totalCount': 0}, 'primaryLanguage': {'name': 'Python'},
             'languages': {'totalSize': 6607, 'totalCount': 1, 'edges': [{'size': 6607, 'node': {'name': 'Python'}}]}},
            {'name': 'Self-Implemented-shell', 'isEmpty': False, 'createdAt': '2018-11-28T06:25:13Z',
             'updatedAt': '2018-11-29T07:07:19Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0},
             'primaryLanguage': {'name': 'C'},
             'languages': {'totalSize': 32111, 'totalCount': 1, 'edges': [{'size': 32111, 'node': {'name': 'C'}}]}},
            {'name': 'sweetknn', 'isEmpty': False, 'createdAt': '2019-12-09T02:49:01Z',
             'updatedAt': '2020-06-16T02:08:03Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Cuda'}, 'languages': {'totalSize': 51303, 'totalCount': 4,
                                                                'edges': [{'size': 43902, 'node': {'name': 'Cuda'}},
                                                                          {'size': 7151, 'node': {'name': 'C++'}},
                                                                          {'size': 168, 'node': {'name': 'Makefile'}},
                                                                          {'size': 82, 'node': {'name': 'Shell'}}]}},
            {'name': 'xv6', 'isEmpty': False, 'createdAt': '2020-05-30T20:57:42Z', 'updatedAt': '2023-02-27T19:52:14Z',
             'forkCount': 0, 'stargazerCount': 2, 'watchers': {'totalCount': 1}, 'primaryLanguage': {'name': 'C'},
             'languages': {'totalSize': 3934093, 'totalCount': 7, 'edges': [{'size': 3332555, 'node': {'name': 'C'}},
                                                                            {'size': 290575,
                                                                             'node': {'name': 'Python'}},
                                                                            {'size': 121043,
                                                                             'node': {'name': 'Assembly'}},
                                                                            {'size': 96121,
                                                                             'node': {'name': 'Makefile'}},
                                                                            {'size': 83088, 'node': {'name': 'C++'}},
                                                                            {'size': 9781, 'node': {'name': 'Perl'}},
                                                                            {'size': 930,
                                                                             'node': {'name': 'Shell'}}]}}],
            'pageInfo': {
                'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMC0wNS0zMFQxNjo1Nzo0Mi0wNDowMM4P-8bN',
                'hasNextPage': True}}}}
        not_fork_collaborator = {'user': {'repositories': {'nodes': [
            {'name': 'WineQualityML', 'isEmpty': False, 'createdAt': '2018-04-24T00:53:51Z',
             'updatedAt': '2018-05-01T22:38:23Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': {'name': 'Python'}, 'languages': {'totalSize': 41353, 'totalCount': 1, 'edges': [
                {'size': 41353, 'node': {'name': 'Python'}}]}},
            {'name': 'qsdmt', 'isEmpty': False, 'createdAt': '2018-12-28T07:54:45Z',
             'updatedAt': '2022-04-01T21:59:49Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': {'name': 'C++'}, 'languages': {'totalSize': 1578318, 'totalCount': 10,
                                                               'edges': [{'size': 829480, 'node': {'name': 'C++'}},
                                                                         {'size': 245682,
                                                                          'node': {'name': 'Jupyter Notebook'}},
                                                                         {'size': 168099, 'node': {'name': 'Python'}},
                                                                         {'size': 153443, 'node': {'name': 'C'}},
                                                                         {'size': 132352, 'node': {'name': 'Shell'}},
                                                                         {'size': 22891, 'node': {'name': 'Perl'}},
                                                                         {'size': 19649, 'node': {'name': 'Makefile'}},
                                                                         {'size': 4371, 'node': {'name': 'Roff'}},
                                                                         {'size': 1187, 'node': {'name': 'M4'}},
                                                                         {'size': 1164,
                                                                          'node': {'name': 'Dockerfile'}}]}},
            {'name': 'CSC724', 'isEmpty': False, 'createdAt': '2020-01-30T01:55:44Z',
             'updatedAt': '2020-07-02T12:03:12Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': {'name': 'Python'}, 'languages': {'totalSize': 43229, 'totalCount': 4,
                                                                  'edges': [{'size': 35696, 'node': {'name': 'Python'}},
                                                                            {'size': 3949, 'node': {'name': 'HTML'}},
                                                                            {'size': 3427, 'node': {'name': 'CSS'}},
                                                                            {'size': 157, 'node': {'name': 'Shell'}}]}},
            {'name': 'social-media-website', 'isEmpty': False, 'createdAt': '2020-08-16T02:28:34Z',
             'updatedAt': '2020-12-16T17:40:17Z', 'forkCount': 4, 'stargazerCount': 1, 'watchers': {'totalCount': 3},
             'primaryLanguage': {'name': 'JavaScript'}, 'languages': {'totalSize': 65630, 'totalCount': 4, 'edges': [
                {'size': 60487, 'node': {'name': 'JavaScript'}}, {'size': 3892, 'node': {'name': 'Sass'}},
                {'size': 968, 'node': {'name': 'Dockerfile'}}, {'size': 283, 'node': {'name': 'HTML'}}]}}],
            'pageInfo': {
                'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMC0wOC0xNVQyMjoyODozNC0wNDowMM4RKGIE',
                'hasNextPage': False}}}}

        count = 0
        for response in self.client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
                                                                                     "pg_size": 5,
                                                                                     "is_fork": True,
                                                                                     "ownership": "OWNER",
                                                                                     "order_by": {"field": "CREATED_AT",
                                                                                                  "direction": "ASC"}}):
            if count == 0:
                assert response == fork_owner
            else:
                break
            count += 1

        count = 0
        for response in self.client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
                                                                                     "pg_size": 5,
                                                                                     "is_fork": True,
                                                                                     "ownership": "COLLABORATOR",
                                                                                     "order_by": {"field": "CREATED_AT",
                                                                                                  "direction": "ASC"}}):
            if count == 0:
                assert response == fork_collaborator
            else:
                break
            count += 1

        count = 0
        for response in self.client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
                                                                                     "pg_size": 5,
                                                                                     "is_fork": False,
                                                                                     "ownership": "OWNER",
                                                                                     "order_by": {"field": "CREATED_AT",
                                                                                                  "direction": "ASC"}}):
            if count == 0:
                assert response == not_fork_owner
            else:
                break
            count += 1

        count = 0
        for response in self.client.execute(query=UserRepositories(), substitutions={"user": "JialinC",
                                                                                     "pg_size": 5,
                                                                                     "is_fork": False,
                                                                                     "ownership": "COLLABORATOR",
                                                                                     "order_by": {"field": "CREATED_AT",
                                                                                                  "direction": "ASC"}}):
            if count == 0:
                assert response == not_fork_collaborator
            else:
                break
            count += 1

    def test_user_repositories_enterprise(self):
        fork_owner = {'user': {'repositories': {'nodes': [
            {'name': 'Onboarding', 'isEmpty': False, 'createdAt': '2021-01-24T04:22:26Z',
             'updatedAt': '2021-01-24T21:49:50Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Java'}, 'languages': {'totalSize': 141674, 'totalCount': 4,
                                                                'edges': [{'size': 111429, 'node': {'name': 'Java'}},
                                                                          {'size': 17695, 'node': {'name': 'HTML'}},
                                                                          {'size': 11605, 'node': {'name': 'Gherkin'}},
                                                                          {'size': 945, 'node': {'name': 'CSS'}}]}},
            {'name': 'GitPractice_517_S21', 'isEmpty': False, 'createdAt': '2021-01-29T22:19:36Z',
             'updatedAt': '2021-01-29T22:19:37Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': None, 'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}},
            {'name': 'AmazeZone.com', 'isEmpty': False, 'createdAt': '2022-02-11T20:14:10Z',
             'updatedAt': '2022-02-11T20:14:11Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 44448, 'totalCount': 6,
                                                                'edges': [{'size': 31337, 'node': {'name': 'Ruby'}},
                                                                          {'size': 8952, 'node': {'name': 'HTML'}},
                                                                          {'size': 1635, 'node': {'name': 'SCSS'}},
                                                                          {'size': 1182,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 709, 'node': {'name': 'CSS'}},
                                                                          {'size': 633,
                                                                           'node': {'name': 'CoffeeScript'}}]}},
            {'name': 'CSC-ECE-GitHub-Practice-Fall-2022', 'isEmpty': False, 'createdAt': '2022-08-26T17:24:57Z',
             'updatedAt': '2022-08-26T17:26:30Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': None, 'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}}], 'pageInfo': {
            'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMi0wOC0yNlQxMzoyNDo1Ny0wNDowMM4AAuyC', 'hasNextPage': False}}}}
        fork_collaborator = {'user': {'repositories': {'nodes': [
            {'name': 'AmazeZone.com', 'isEmpty': False, 'createdAt': '2021-09-10T18:07:34Z',
             'updatedAt': '2021-09-10T19:55:11Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 66751, 'totalCount': 6,
                                                                'edges': [{'size': 45154, 'node': {'name': 'Ruby'}},
                                                                          {'size': 16894, 'node': {'name': 'HTML'}},
                                                                          {'size': 2179, 'node': {'name': 'SCSS'}},
                                                                          {'size': 1182,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 709, 'node': {'name': 'CSS'}},
                                                                          {'size': 633,
                                                                           'node': {'name': 'CoffeeScript'}}]}},
            {'name': 'AmazeZone.com', 'isEmpty': False, 'createdAt': '2022-02-04T19:07:00Z',
             'updatedAt': '2022-02-04T20:19:38Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 67499, 'totalCount': 6,
                                                                'edges': [{'size': 46010, 'node': {'name': 'Ruby'}},
                                                                          {'size': 16786, 'node': {'name': 'HTML'}},
                                                                          {'size': 2179, 'node': {'name': 'SCSS'}},
                                                                          {'size': 1182,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 709, 'node': {'name': 'CSS'}},
                                                                          {'size': 633,
                                                                           'node': {'name': 'CoffeeScript'}}]}},
            {'name': 'CSC-ECE-GitHub-Practice-Fall-2022', 'isEmpty': False, 'createdAt': '2022-08-29T13:49:47Z',
             'updatedAt': '2022-08-30T13:45:28Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': None, 'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}},
            {'name': 'AmazeZone.com', 'isEmpty': False, 'createdAt': '2022-09-16T17:53:30Z',
             'updatedAt': '2022-09-16T20:08:27Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 68465, 'totalCount': 6,
                                                                'edges': [{'size': 45742, 'node': {'name': 'Ruby'}},
                                                                          {'size': 17387, 'node': {'name': 'HTML'}},
                                                                          {'size': 2179, 'node': {'name': 'SCSS'}},
                                                                          {'size': 1266,
                                                                           'node': {'name': 'CoffeeScript'}},
                                                                          {'size': 1182,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 709, 'node': {'name': 'CSS'}}]}},
            {'name': 'AmazeZone.com', 'isEmpty': False, 'createdAt': '2023-02-04T22:11:22Z',
             'updatedAt': '2023-02-04T22:36:14Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 69309, 'totalCount': 6,
                                                                'edges': [{'size': 46914, 'node': {'name': 'Ruby'}},
                                                                          {'size': 17626, 'node': {'name': 'HTML'}},
                                                                          {'size': 2189, 'node': {'name': 'SCSS'}},
                                                                          {'size': 1214,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 724, 'node': {'name': 'CSS'}},
                                                                          {'size': 642,
                                                                           'node': {'name': 'CoffeeScript'}}]}}],
            'pageInfo': {
                'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMy0wMi0wNFQxNzoxMToyMi0wNTowMM4AAzvo',
                'hasNextPage': True}}}}
        not_fork_owner = {'user': {'repositories': {'nodes': [
            {'name': 'haha', 'isEmpty': True, 'createdAt': '2020-05-30T19:38:14Z', 'updatedAt': '2020-05-30T19:38:14Z',
             'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1}, 'primaryLanguage': None,
             'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}},
            {'name': 'CSC_ECE_517_Assignment_1', 'isEmpty': False, 'createdAt': '2021-01-29T19:52:29Z',
             'updatedAt': '2021-01-30T04:38:11Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': None, 'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}},
            {'name': 'CrashAirline', 'isEmpty': False, 'createdAt': '2021-02-15T05:22:18Z',
             'updatedAt': '2021-02-23T22:19:50Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 108219, 'totalCount': 5,
                                                                'edges': [{'size': 71811, 'node': {'name': 'Ruby'}},
                                                                          {'size': 31331, 'node': {'name': 'HTML'}},
                                                                          {'size': 3471,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 897, 'node': {'name': 'SCSS'}},
                                                                          {'size': 709, 'node': {'name': 'CSS'}}]}},
            {'name': '517Project2', 'isEmpty': False, 'createdAt': '2021-02-23T23:03:40Z',
             'updatedAt': '2021-03-04T05:53:56Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Ruby'}, 'languages': {'totalSize': 134324, 'totalCount': 5,
                                                                'edges': [{'size': 92144, 'node': {'name': 'Ruby'}},
                                                                          {'size': 37103, 'node': {'name': 'HTML'}},
                                                                          {'size': 3471,
                                                                           'node': {'name': 'JavaScript'}},
                                                                          {'size': 897, 'node': {'name': 'SCSS'}},
                                                                          {'size': 709, 'node': {'name': 'CSS'}}]}},
            {'name': 'GitHub_GraphQL', 'isEmpty': False, 'createdAt': '2023-01-30T18:03:01Z',
             'updatedAt': '2023-01-30T18:06:36Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Python'}, 'languages': {'totalSize': 49566, 'totalCount': 1, 'edges': [
                {'size': 49566, 'node': {'name': 'Python'}}]}}], 'pageInfo': {
            'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMy0wMS0zMFQxMzowMzowMS0wNTowMM4AAzqi', 'hasNextPage': True}}}}
        not_fork_collaborator = {'user': {'repositories': {'nodes': [
            {'name': 'customized_php', 'isEmpty': False, 'createdAt': '2019-04-22T14:14:49Z',
             'updatedAt': '2020-08-17T00:54:54Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 0},
             'primaryLanguage': {'name': 'C++'}, 'languages': {'totalSize': 3878604, 'totalCount': 6,
                                                               'edges': [{'size': 1940505, 'node': {'name': 'C++'}},
                                                                         {'size': 883531, 'node': {'name': 'TeX'}},
                                                                         {'size': 683503, 'node': {'name': 'C'}},
                                                                         {'size': 178694, 'node': {'name': 'Python'}},
                                                                         {'size': 177266,
                                                                          'node': {'name': 'Objective-C'}},
                                                                         {'size': 15105, 'node': {'name': 'PHP'}}]}},
            {'name': 'Environment-Setup', 'isEmpty': False, 'createdAt': '2019-11-26T19:06:39Z',
             'updatedAt': '2022-04-12T01:49:21Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': None, 'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}},
            {'name': 'ReqRacer', 'isEmpty': False, 'createdAt': '2020-02-02T00:12:14Z',
             'updatedAt': '2020-05-27T04:22:12Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 1},
             'primaryLanguage': {'name': 'Python'}, 'languages': {'totalSize': 271040, 'totalCount': 1, 'edges': [
                {'size': 271040, 'node': {'name': 'Python'}}]}},
            {'name': 'qsdmt-paper', 'isEmpty': False, 'createdAt': '2020-05-05T06:11:05Z',
             'updatedAt': '2020-06-02T14:53:09Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': {'name': 'TeX'}, 'languages': {'totalSize': 104559, 'totalCount': 3,
                                                               'edges': [{'size': 103914, 'node': {'name': 'TeX'}},
                                                                         {'size': 348, 'node': {'name': 'Makefile'}},
                                                                         {'size': 297, 'node': {'name': 'Python'}}]}},
            {'name': 'CSC_ECE_517_Assignment_1', 'isEmpty': False, 'createdAt': '2021-08-20T18:28:21Z',
             'updatedAt': '2021-08-27T17:10:18Z', 'forkCount': 0, 'stargazerCount': 0, 'watchers': {'totalCount': 2},
             'primaryLanguage': None, 'languages': {'totalSize': 0, 'totalCount': 0, 'edges': []}}], 'pageInfo': {
            'endCursor': 'Y3Vyc29yOnYyOpK5MjAyMS0wOC0yMFQxNDoyODoyMS0wNDowMM4AAlTb', 'hasNextPage': True}}}}

        count = 0
        for response in self.enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
                                                                                                "pg_size": 5,
                                                                                                "is_fork": True,
                                                                                                "ownership": "OWNER",
                                                                                                "order_by": {
                                                                                                    "field": "CREATED_AT",
                                                                                                    "direction": "ASC"}}):
            if count == 0:
                assert response == fork_owner
            else:
                break
            count += 1

        count = 0
        for response in self.enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
                                                                                                "pg_size": 5,
                                                                                                "is_fork": True,
                                                                                                "ownership": "COLLABORATOR",
                                                                                                "order_by": {
                                                                                                    "field": "CREATED_AT",
                                                                                                    "direction": "ASC"}}):
            if count == 0:
                assert response == fork_collaborator
            else:
                break
            count += 1

        count = 0
        for response in self.enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
                                                                                                "pg_size": 5,
                                                                                                "is_fork": False,
                                                                                                "ownership": "OWNER",
                                                                                                "order_by": {
                                                                                                    "field": "CREATED_AT",
                                                                                                    "direction": "ASC"}}):
            if count == 0:
                assert response == not_fork_owner
            else:
                break
            count += 1

        count = 0
        for response in self.enterprise_client.execute(query=UserRepositories(), substitutions={"user": "jcui9",
                                                                                                "pg_size": 5,
                                                                                                "is_fork": False,
                                                                                                "ownership": "COLLABORATOR",
                                                                                                "order_by": {
                                                                                                    "field": "CREATED_AT",
                                                                                                    "direction": "ASC"}}):
            if count == 0:
                assert response == not_fork_collaborator
            else:
                break
            count += 1
