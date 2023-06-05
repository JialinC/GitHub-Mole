import os
from datetime import datetime, timedelta
from string import Template

import pytest

import helper
import metrics_commits
import metrics_no_commits
import user_comments

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TEST_USER = os.environ.get("TEST_USER", "ppkhawas")
TEST_USER_2 = os.environ.get("TEST_USER_2", "jcui9")

TEST_INPUT_FILE_PATH = os.environ.get("TEST_INPUT_FILE_PATH", "../etc/data/test_data_ncsu.csv")
TEST_OUTPUT_FILE_PATH = os.environ.get("TEST_OUTPUT_FILE_PATH", "../test_out.csv")


class TestHelper:
    def test_one(self):
        header = helper.get_auth_header()

        assert GITHUB_TOKEN in header['Authorization']

    def test_two(self):
        abs_path_one = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)

        assert os.path.exists(abs_path_one)

    def test_three(self):
        abs_path_two = helper.get_abs_path('test')

        assert not os.path.exists(abs_path_two)

    def test_four(self):
        file_name = helper.generate_file_name()

        assert len(file_name) == 6

    def test_five(self):
        query1 = Template(
            """
            query{
                user(login: "$test_user"){
                login
                }
            }
            """
        ).substitute(test_user=TEST_USER)

        assert TEST_USER == helper.execute_query(query1)['user']['login']

    def test_six(self):
        query2 = Template(
            """
            quer{
                user(login: "$test_user"){
                login
                }
            }
            """
        ).substitute(test_user=TEST_USER)

        with pytest.raises(Exception) as e_info:
            helper.execute_query(query2)

    def test_seven(self):
        assert TEST_USER == helper.get_login(TEST_USER)['user']['login']

    def test_eight(self):
        assert 200 == helper.rate_limit()['rateLimit']['limit']

    def test_nine(self):
        time = "1995-05-28T00:00:00Z"

        assert "1996-05-28T00:00:00Z" == helper.add_a_year(time)

    def test_ten(self):
        x = "2021-06-01T00:00:00Z"
        y = "2021-01-01T00:00:00Z"
        z = "2022-01-01T00:00:00Z"

        assert helper.in_time_period(x, y, z)


class TestMetricsNoCommits:
    def test_one(self):
        response = metrics_no_commits.get_data(TEST_USER)['user']['login']

        assert response == TEST_USER

    def test_two(self):
        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        metrics_no_commits.log_data(TEST_USER, abs_path)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        first_word = last_line.split(',')[0]

        assert first_word == TEST_USER

    def test_three(self):
        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        metrics_no_commits.log_data('gsdgfsdxrrt', abs_path)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == 'gsdgfsdxrrt do not exist\n'

    def test_four(self):
        metrics_no_commits.driver(TEST_INPUT_FILE_PATH, TEST_OUTPUT_FILE_PATH)
        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)

        with open(abs_path, 'r') as f:
            last_10_lines = f.readlines()[-10:]

        print(last_10_lines)

        assert last_10_lines[-4].split(',')[0] == TEST_USER \
               and last_10_lines[-2].split(',')[0] == TEST_USER_2 \
               and last_10_lines[-1] == 'jdfsdbfadnotexist do not exist\n'


class TestMetricsCommits:
    def test_one(self):
        start_time = "2021-01-01T00:00:00Z"
        end_time = "2022-01-01T00:00:00Z"

        restrictedContributionsCount = metrics_commits.get_data_by_time_period(
            TEST_USER, start_time, end_time
        )['user']['contributionsCollection']['restrictedContributionsCount']

        assert restrictedContributionsCount == 0

    def test_two(self):
        start_time = "2021-01-01T00:00:00Z"
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        metrics_commits.log_data(TEST_USER, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line.split(',')[1] == start_time and last_line.split(',')[2] == end_time

    def test_three(self):
        creation_date = helper.get_login(TEST_USER)["user"]["createdAt"]
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        metrics_commits.log_data(TEST_USER, abs_path, None, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line.split(',')[1] == creation_date and last_line.split(',')[2] == end_time

    def test_four(self):
        start_time = "2021-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        metrics_commits.log_data(TEST_USER, abs_path, start_time, None)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        testtime = datetime.strptime(last_line.split(',')[2], '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.now()
        elapsed = now - testtime

        assert last_line.split(',')[1] == start_time and elapsed < timedelta(seconds=5)

    def test_five(self):
        creation_date = helper.get_login(TEST_USER)["user"]["createdAt"]

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        metrics_commits.log_data(TEST_USER, abs_path, None, None)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        testtime = datetime.strptime(last_line.split(',')[2], '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.now()
        elapsed = now - testtime

        assert last_line.split(',')[1] == creation_date and elapsed < timedelta(seconds=5)

    def test_six(self):
        start_time = "2021-01-01T00:00:00Z"
        end_time = "2022-01-01T00:00:00Z"

        metrics_commits.driver(TEST_INPUT_FILE_PATH, TEST_OUTPUT_FILE_PATH, start_time, end_time)
        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)

        with open(abs_path, 'r') as f:
            last_10_lines = f.readlines()[-10:]

        assert last_10_lines[-4].split(',')[0] == TEST_USER \
               and last_10_lines[-2].split(',')[0] == TEST_USER_2 \
               and last_10_lines[-1] == 'jdfsdbfadnotexist do not exist\n'


class TestUserComments:
    def test_one(self):
        comment_type = 'commitComments'
        dic = user_comments.user_comments_history_init(TEST_USER, comment_type)['user']

        assert list(dic.keys())[1] == comment_type

    def test_two(self):
        comment_type = 'issueComments'
        dic = user_comments.user_comments_history_init(TEST_USER, comment_type)['user']

        assert list(dic.keys())[1] == comment_type

    def test_three(self):
        comment_type = 'gistComments'
        dic = user_comments.user_comments_history_init(TEST_USER, comment_type)['user']

        assert list(dic.keys())[1] == comment_type

    def test_four(self):
        comment_type = 'repositoryDiscussionComments'
        dic = user_comments.user_comments_history_init(TEST_USER, comment_type)['user']

        assert list(dic.keys())[1] == comment_type

    def test_five(self):
        comment_type = 'commitComments'

        init_query = user_comments.user_comments_history_init(TEST_USER, comment_type)
        end_cursor = init_query["user"][comment_type]["pageInfo"]["endCursor"]

        dic = user_comments.user_comments_history_page(TEST_USER, comment_type, end_cursor)

        if end_cursor is None:
            assert dic['user'] is None
        else:
            assert list(dic['user'].keys())[1] == comment_type

    def test_six(self):
        comment_type = 'issueComments'

        init_query = user_comments.user_comments_history_init(TEST_USER, comment_type)
        end_cursor = init_query["user"][comment_type]["pageInfo"]["endCursor"]

        dic = user_comments.user_comments_history_page(TEST_USER, comment_type, end_cursor)

        if end_cursor is None:
            assert dic['user'] is None
        else:
            assert list(dic['user'].keys())[1] == comment_type

    def test_seven(self):
        comment_type = 'gistComments'

        init_query = user_comments.user_comments_history_init(TEST_USER, comment_type)
        end_cursor = init_query["user"][comment_type]["pageInfo"]["endCursor"]

        dic = user_comments.user_comments_history_page(TEST_USER, comment_type, end_cursor)

        if end_cursor is None:
            assert dic['user'] is None
        else:
            assert list(dic['user'].keys())[1] == comment_type

    def test_eight(self):
        comment_type = 'repositoryDiscussionComments'

        init_query = user_comments.user_comments_history_init(TEST_USER, comment_type)
        end_cursor = init_query["user"][comment_type]["pageInfo"]["endCursor"]

        dic = user_comments.user_comments_history_page(TEST_USER, comment_type, end_cursor)

        if end_cursor is None:
            assert dic['user'] is None
        else:
            assert list(dic['user'].keys())[1] == comment_type

    def test_nine(self):
        comment_type = 'commitComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_ten(self):
        comment_type = 'issueComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_eleven(self):
        comment_type = 'gistComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_twelve(self):
        comment_type = 'repositoryDiscussionComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_thirteen(self):
        comment_type = 'commitComments'

        start_time = None
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_fourteen(self):
        comment_type = 'issueComments'

        start_time = None
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_fifteen(self):
        comment_type = 'gistComments'

        start_time = None
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_sixteen(self):
        comment_type = 'repositoryDiscussionComments'

        start_time = None
        end_time = "2022-01-01T00:00:00Z"

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_seventeen(self):
        comment_type = 'commitComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_eighteen(self):
        comment_type = 'issueComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_nineteen(self):
        comment_type = 'gistComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_twenty(self):
        comment_type = 'repositoryDiscussionComments'

        start_time = "2021-01-01T00:00:00Z"
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_twentyone(self):
        comment_type = 'commitComments'

        start_time = None
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_twentytwo(self):
        comment_type = 'issueComments'

        start_time = None
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_twentythree(self):
        comment_type = 'gistComments'

        start_time = None
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)

    def test_twentyfour(self):
        comment_type = 'repositoryDiscussionComments'

        start_time = None
        end_time = None

        abs_path = helper.get_abs_path(TEST_OUTPUT_FILE_PATH)
        user_comments.log_data(TEST_USER, comment_type, abs_path, start_time, end_time)

        with open(abs_path, 'r') as f:
            last_line = f.readlines()[-1]

        assert last_line == Template(
            '$test_user does not have $comment_type\n'
        ).substitute(test_user=TEST_USER, comment_type=comment_type)
