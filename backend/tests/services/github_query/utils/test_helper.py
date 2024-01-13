import pytest
import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from backend.app.services.github_query.github_graphql.client import Client
from backend.app.services.github_query.github_graphql.query import Query
from backend.app.services.github_query.utils.helper import print_methods, print_attr, get_abs_path, generate_file_name, add_by_days, minus_by_days, in_time_period, created_before, created_after, write_csv, get_owner_and_name, have_rate_limit

class TestUtilityFunctions:
    def test_get_abs_path(mock_file_path):
        file_name = "test.csv"
        script_path = os.path.abspath(__file__)
        script_dir = os.path.split(script_path)[0]
        rel_file_path = "query_result\\" + file_name
        expected_path = os.path.join(script_dir, rel_file_path)
        expected_path = expected_path.replace('tests', 'app')
        assert get_abs_path(file_name) == expected_path

    def test_generate_file_name(self):
        file_name = generate_file_name()
        assert len(file_name) == 6, "File name should be 6 characters long."
        assert file_name.isalnum(), "File name should be alphanumeric."

    def test_add_by_days(self):
        original_time = "2021-01-01T00:00:00Z"
        expected_time = (datetime.strptime(original_time, "%Y-%m-%dT%H:%M:%SZ") + timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
        assert add_by_days(original_time,365) == expected_time, "Should add one year to the input time string."
    
    def test_minus_by_days(self):
        original_time = "2021-01-01T00:00:00Z"
        expected_time = (datetime.strptime(original_time, "%Y-%m-%dT%H:%M:%SZ") - timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
        assert minus_by_days(original_time,365) == expected_time, "Should minus one year to the input time string."

    def test_in_time_period(self):
        start = "2021-01-01T00:00:00Z"
        end = "2021-12-31T23:59:59Z"
        assert in_time_period("2021-06-01T12:00:00Z", start, end) is True, "Should be within the time period."
        assert in_time_period("2020-01-01T00:00:00Z", start, end) is False, "Should be outside the time period."

    def test_created_before(self):
        assert created_before("2021-01-01T00:00:00Z", "2022-01-01T00:00:00Z") is True, "Created should be before the time."
        assert created_before("2023-01-01T00:00:00Z", "2022-01-01T00:00:00Z") is False, "Created should not be before the time."
    
    def test_created_after(self):
        assert created_after("2022-01-01T00:00:00Z", "2021-01-01T00:00:00Z") is True, "Created should be after the time."
        assert created_after("2022-01-01T00:00:00Z", "2023-01-01T00:00:00Z") is False, "Created should not be after the time."

    def test_write_csv(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
            data_row = "test,data,row"
            write_csv(tmp.name, data_row)
            tmp.seek(0)
            content = tmp.read()
            assert content.strip() == data_row, "The written content should match the input data row."

    def test_get_owner_and_name(self):
        valid_link = "https://github.com/owner/repo"
        owner, repo = get_owner_and_name(valid_link)
        assert owner == "owner" and repo == "repo", "Should correctly parse owner and repo from the link."

    def test_have_rate_limit_enough(self):
        """
        Test have_rate_limit returns True when enough rate limit is available
        """
        # Setup Mock Client and Query
        mock_client = MagicMock(spec=Client)
        mock_query = MagicMock(spec=Query)

        # Mock the Query substitution to return a predictable string
        mock_query_string = "query { rateLimit { cost } }"
        mock_query.substitute.return_value = mock_query_string

        # Mock the client's execute method to return controlled rate limit info
        mock_rate_limit_info = {
            'rateLimit': {
                'cost': 1,
                'remaining': 10,  # Ensure the cost is less than remaining - 5
                'resetAt': "2023-01-01T00:00:00Z"
            }
        }
        mock_client.execute.return_value = mock_rate_limit_info

        # Call have_rate_limit and assert it returns True and reset time
        assert have_rate_limit(mock_client, mock_query, {}) == [True, "2023-01-01T00:00:00Z"], \
            "Should indicate enough rate limit is available"

    def test_have_rate_limit_not_enough(self):
        """
        Test have_rate_limit returns False when not enough rate limit is available
        """
        # Setup Mock Client and Query with similar mocking strategy as above
        mock_client = MagicMock(spec=Client)
        mock_query = MagicMock(spec=Query)
        mock_query.substitute.return_value = "query { rateLimit { cost } }"

        # Mock the client's execute method to return controlled rate limit info
        mock_rate_limit_info = {
            'rateLimit': {
                'cost': 10,
                'remaining': 10,  # Ensure the cost is not less than remaining - 5
                'resetAt': "2023-01-01T00:00:00Z"
            }
        }
        mock_client.execute.return_value = mock_rate_limit_info

        # Call have_rate_limit and assert it returns False and reset time
        assert have_rate_limit(mock_client, mock_query, {}) == [False, "2023-01-01T00:00:00Z"], \
            "Should indicate not enough rate limit is available"



