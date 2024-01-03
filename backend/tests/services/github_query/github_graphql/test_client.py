import pytest
import requests_mock
from unittest.mock import MagicMock
from datetime import datetime
from requests.exceptions import Timeout
from backend.app.services.github_query.github_graphql.client import Client, InvalidAuthenticationError, QueryFailedException, RESTClient
from backend.app.services.github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator 
from backend.app.services.github_query.github_graphql.query import Query, PaginatedQuery

@pytest.fixture
def valid_token():
    return "valid_token_123"

@pytest.fixture
def authenticator(valid_token):
    return PersonalAccessTokenAuthenticator(token=valid_token)

@pytest.fixture
def github_client(authenticator):
    return Client(authenticator=authenticator)

class TestClient:
    def test_client_without_authenticator(self):
        """Test that client raises error when no authenticator is provided"""
        with pytest.raises(InvalidAuthenticationError):
            Client()  # No authenticator provided

    def test_client_initialization(self, github_client):
        """Test that the client is correctly initialized with the given authenticator"""
        assert github_client._authenticator is not None, "Authenticator should be set."

    def test_client_base_path(self, github_client):
        """Test that the base path is correctly constructed"""
        assert "api.github.com" in github_client._base_path(), "Base path should include the host."
    
    def test_generate_headers(self, github_client, authenticator):
        """Test that headers are correctly generated including authorization and additional headers."""
        additional_headers = {"Custom-Header": "CustomValue"}
        expected_headers = authenticator.get_authorization_header()
        expected_headers.update(additional_headers)

        assert github_client._generate_headers(**additional_headers) == expected_headers, "Headers should include both authenticator and additional headers."

    def test_retry_success(self, github_client, requests_mock):
        """Test that retry_request succeeds after a retry."""
        # Mock the request to timeout once then succeed
        requests_mock.register_uri('POST', github_client._base_path(), [
            {'exc': Timeout},
            {'json': {'data': 'success'}, 'status_code': 200}
        ])
        
        response = github_client._retry_request(2, 1, "query { viewer { login }}", {})
        assert response.json() == {'data': 'success'}, "Should succeed on the second attempt."

    def test_retry_timeout(self, github_client, requests_mock):
        """Test that retry_request gives up after attempts are exhausted."""
        # Mock the request to timeout
        requests_mock.register_uri('POST', github_client._base_path(), [
            {'exc': Timeout},
            {'exc': Timeout}
        ])
        
        with pytest.raises(Timeout):
            github_client._retry_request(2, 1, "query { viewer { login }}", {})

    def test_execute_success(self, github_client, requests_mock):
        """Test successful execution of a query."""
        # Mock the rate limit pre-check and the actual query execution
        requests_mock.post(github_client._base_path(), [
            {'json': {"data": {"rateLimit": {"cost": 1, "remaining": 5000, "resetAt": "2021-01-01T00:00:00Z"}}}, 'status_code': 200},
            {'json': {"data": "query success"}, 'status_code': 200}
        ])
        response = github_client._execute("query { viewer { login }}", {})
        assert response == "query success", "Execute should return success on valid response."

    def test_execute_rate_limit_exceeded(self, github_client, requests_mock):
        """Test execution of a query leading to waiting for rate limit reset."""
        # Set specific values for cost, remaining, and resetAt
        mock_cost = 10
        mock_remaining = 14  # Ensure remaining - 5 < mock_cost
        mock_reset_at = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        # Mock rate limit response
        mock_rate_limit_response = {
            "data": {
                "rateLimit": {
                    "cost": mock_cost,
                    "remaining": mock_remaining,
                    "resetAt": mock_reset_at
                }
            }
        }

        # Setup requests_mock to simulate the rate limit response and any subsequent requests
        base_path = github_client._base_path()
        requests_mock.post(base_path, [
            {'json': mock_rate_limit_response, 'status_code': 200},
            {'json': {"data": "query success"}, 'status_code': 200}
        ])
        response = github_client._execute("query { viewer { login }}", {})
        assert response == "query success", "Execute should return success on valid response."

    def test_execute_query_failed(self, github_client, requests_mock):
        """Test execution of a query leading to QueryFailedException with retries."""
        # Mock a failed query response for each retry attempt
        requests_mock.post(github_client._base_path(), [
            {'json': {"data": {"rateLimit": {"cost": 1, "remaining": 5000, "resetAt": "2021-01-01T00:00:00Z"}}}, 'status_code': 200},
            {"json": {"error": "bad request"}, "status_code": 400}
        ])
        # Expecting QueryFailedException after all retries have been exhausted
        with pytest.raises(QueryFailedException):
            github_client._execute("query { viewer { login }}", {})
    
    def test_execution_generator(self, github_client):
        """Test that _execution_generator correctly handles paginated responses."""
        # Setup a mock paginated query
        query = MagicMock()
        query.paginator.has_next.side_effect = [True, True, False]  # Simulate 2 pages of results, then stop
        query.path = []  # Example path, adjust based on your actual usage

        # Mock the _execute method to return simulated page results
        github_client._execute = MagicMock()
        github_client._execute.side_effect = [
            {"pageInfo": {"endCursor": "cursor1", "hasNextPage": True}, "nodes": [{"edges": "data1"}]},
            {"pageInfo": {"endCursor": "cursor2", "hasNextPage": False}, "nodes": [{"edges": "data2"}]}
        ]

        # Mock the update_paginator method to reflect the changing state of pagination
        query.paginator.update_paginator = MagicMock()

        # Collect all results from the generator
        results = list(github_client._execution_generator(query, {}))

        # Assertions
        assert len(results) == 2, "Should yield two results for the two pages"
        assert results[0]['nodes'][0]['edges'] == "data1", "First result should match first mocked response"
        assert results[1]['nodes'][0]['edges'] == "data2", "Second result should match second mocked response"

        # Ensure update_paginator was called correctly
        assert query.paginator.update_paginator.call_count == 2, "update_paginator should be called twice, once per page"
        query.paginator.update_paginator.assert_called_with(False, "cursor2")  # Last call should reflect the end of pagination

    def test_client_execute_success(self, github_client, requests_mock):
        """Test successful execution of a query"""
        requests_mock.post(github_client._base_path(), [
            {'json': {"data": {"rateLimit": {"cost": 1, "remaining": 5000, "resetAt": "2021-01-01T00:00:00Z"}}}, 'status_code': 200},
            {'json': {"data": "query success"}, 'status_code': 200}
        ])
        response = github_client.execute(Query("query { viewer { login }}"), {})
        assert response == "query success", "Execute should return success on valid response."

    def test_client_execute_failed(self, github_client, requests_mock):
        """Test that a failed query raises QueryFailedException"""
        requests_mock.post(github_client._base_path(), [
            {'json': {"data": {"rateLimit": {"cost": 1, "remaining": 5000, "resetAt": "2021-01-01T00:00:00Z"}}}, 'status_code': 200},
            {"json": {"error": "bad request"}, "status_code": 400}
        ])
        with pytest.raises(QueryFailedException) as excinfo:
            github_client.execute(Query("query { viewer { login }}"), {})
        assert "Query failed with code" in str(excinfo.value), "QueryFailedException should contain the right error message."