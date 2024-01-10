import re
import time
from datetime import datetime
from random import randint
from string import Template
from typing import Union, Optional, Dict, Any, Generator
import requests
from requests.exceptions import Timeout, RequestException
from requests import Response
from backend.app.services.github_query.github_graphql.authentication import Authenticator
from backend.app.services.github_query.github_graphql.query import Query, PaginatedQuery
from backend.app.services.github_query.queries.costs.query_cost import QueryCost

class InvalidAuthenticationError(Exception):
    """Exception raised when an authentication object is invalid or not provided."""
    pass

class QueryFailedException(Exception):
    """
    Exception raised when a GraphQL query fails to execute properly.
    This can be due to various reasons including network issues or logical errors in query construction.
    """
    def __init__(self, response: Response, query: Optional[str] = None) -> None:
        # Initializing the exception with the response and query that caused the failure
        self.response = response
        self.query = query
        # Constructing a detailed error message
        if query:
            message = f"Query failed with code {response.status_code}. Query: {query}. Response: {response.text}"
        else:
            message = f"Query failed with code {response.status_code}. Path: {response.request.path_url}. Response: {response.text}"
        super().__init__(message)

class Client:
    """
    Client is a class that handles making GraphQL queries to a GitHub instance using the provided authentication.
    It manages request construction, execution, and error handling, along with support for pagination.
    """
    def __init__(self, protocol: str = "https", host: str = "api.github.com", is_enterprise: bool = False, authenticator: Optional[Authenticator] = None) -> None:
        """
        Initializes the client with the necessary configuration and authentication.

        Args:
            protocol (str): The protocol to use for connecting to the GitHub server (usually https).
            host (str): The host address of the GitHub server.
            is_enterprise (bool): Indicates whether the client is connecting to a GitHub Enterprise instance.
            authenticator (Optional[Authenticator]): The authenticator instance for handling authentication.

        Raises:
            InvalidAuthenticationError: If no authenticator is provided or if the provided authenticator is invalid.
        """
        self._protocol = protocol
        self._host = host
        self._is_enterprise = is_enterprise

        if authenticator is None:
            raise InvalidAuthenticationError("Authentication needs to be specified")
        self._authenticator = authenticator
        # Instantiating the RESTClient with the same configuration for REST API operations
        self.rest = RESTClient(protocol=self._protocol, host=self._host, is_enterprise=self._is_enterprise, authenticator=self._authenticator)
        
    def _base_path(self) -> str:
        """
        Constructs the base URL path for the GitHub GraphQL API.

        Returns:
            str: The base URL path for the GitHub GraphQL API.
        """
        return (
            f"{self._protocol}://{self._host}/api/graphql"
            if self._is_enterprise else
            f"{self._protocol}://{self._host}/graphql"
        )

    def _generate_headers(self, **kwargs) -> Dict[str, str]:
        """
        Generates the necessary headers for making a GraphQL request, including authentication headers.

        Args:
            **kwargs: Additional headers to include in the request.

        Returns:
            Dict[str, str]: A dictionary of headers for the request.
        """
        headers = self._authenticator.get_authorization_header()
        headers.update(kwargs)
        return headers

    def _retry_request(self, retry_attempts: int, timeout_seconds: int, query: Union[str, Query], substitutions: Dict[str, Any]) -> Response:
        """
        Tries to send a request multiple times until it succeeds or the retry limit is reached.

        Args:
            retry_attempts (int): The number of times to retry the request before giving up.
            timeout_seconds (int): The number of seconds to wait for a response before timing out.
            query (Union[str, Query]): The GraphQL query to execute.
            substitutions (Dict[str, Any]): Substitutions to apply to the query template.

        Returns:
            Response: The server's response to the HTTP request.

        Raises:
            Timeout: If all retry attempts are exhausted and the request keeps timing out.
        """
        last_exception = None
        response = None
        for _ in range(retry_attempts):
            try:
                response = requests.post(
                    self._base_path(),
                    json={
                        'query': Template(query).substitute(**substitutions) if isinstance(query, str) else query.substitute(**substitutions)
                    },
                    headers=self._generate_headers(),
                    timeout=timeout_seconds
                )
                if response.status_code == 200:
                    return response
            except Timeout as e:
                last_exception = e
                print("Request timed out. Retrying...")
        # If this point is reached, all retries have been exhausted
        if not last_exception:
            raise QueryFailedException(query=query, response=response)
        raise Timeout("All retry attempts exhausted.")

    def _execute(self, query: Union[str, Query], substitutions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a query with the given substitutions and handles response processing and error checking.

        Args:
            query (Union[str, Query]): The GraphQL query to execute.
            substitutions (Dict[str, Any]): Substitutions to apply to the query template.

        Returns:
            Dict[str, Any]: The parsed JSON response from the server.

        Raises:
            QueryFailedException: If the query execution fails or returns errors.
        """
        query_string = Template(query).substitute(**substitutions) if isinstance(query, str) else query.substitute(**substitutions)
        match = re.search(r'query\s*{(?P<content>.+)}', query_string)
        # pre-calculate the cost of the upcoming graphql query
        rate_query = QueryCost(match.group('content'))
        rate_limit = self._retry_request(3, 10, rate_query, {"dryrun": True})
        rate_limit = rate_limit.json()["data"]["rateLimit"]
        cost, remaining, reset_at = rate_limit['cost'], rate_limit['remaining'], rate_limit['resetAt']
        # if the cost of the upcoming graphql query larger than avaliable ratelimit, wait till ratelimit reset
        if cost > remaining - 5:
            current_time = datetime.utcnow()
            time_format = '%Y-%m-%dT%H:%M:%SZ'
            reset_at = datetime.strptime(reset_at, time_format)
            time_diff = reset_at - current_time
            seconds = time_diff.total_seconds()
            print(f"stop at {current_time}s.")
            print(f"waiting for {seconds}s.")
            print(f"reset at {reset_at}s.")
            time.sleep(seconds + 5)

        response = self._retry_request(3, 10, query, substitutions)
        try:
            json_response = response.json()
        except RequestException:
            raise QueryFailedException(query=query, response=response)

        if response.status_code == 200 and "errors" not in json_response:
            return json_response["data"]
        else:
            raise QueryFailedException(query=query, response=response)

    def execute(self, query: Union[str, Query, PaginatedQuery], substitutions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public method to execute a non-paginated or paginated query.

        Args:
            query (Union[str, Query, PaginatedQuery]): The GraphQL query to execute.
            substitutions (Dict[str, Any]): Substitutions to apply to the query template.

        Returns:
            Dict[str, Any]: The parsed JSON response from the server.
        """
        if isinstance(query, PaginatedQuery):
            return self._execution_generator(query, substitutions)

        return self._execute(query, substitutions)

    def _execution_generator(self, query: Union[Query, PaginatedQuery], substitutions: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """
        Handles the iteration over paginated query results, yielding each page's data as it's fetched.

        Args:
            query (Union[Query, PaginatedQuery]): The paginated GraphQL query to execute.
            substitutions (Dict[str, Any]): Substitutions to apply to the query template.

        Returns:
            Generator[Dict[str, Any], None, None]: A generator yielding each page's data as a dictionary.
        """
        while query.paginator.has_next():
            response = self._execute(query, substitutions)
            curr_node = response
            print(curr_node)

            for field_name in query.path:
                curr_node = curr_node[Template(field_name).substitute(**substitutions)]

            end_cursor = curr_node["pageInfo"]["endCursor"]
            has_next_page = curr_node["pageInfo"]["hasNextPage"]
            query.paginator.update_paginator(has_next_page, end_cursor)
            yield response

# future work
class RESTClient:
    """
    A client for interacting with the GitHub REST API.
    Handles the construction and execution of RESTful requests with provided authentication.
    """
    def __init__(self, protocol: str = "https", host: str = "api.github.com", is_enterprise: bool = False, authenticator: Authenticator = None) -> None:
        """
        Initialization with protocol, host, and whether the GitHub instance is Enterprise
        Requires an Authenticator to be provided for handling authentication
        Args:
            protocol: Protocol for the server
            host: Host for the server
            is_enterprise: Is the host running on Enterprise Version?
            authenticator: Authenticator for the client
        """
        self._protocol = protocol
        self._host = host
        self._is_enterprise = is_enterprise

        if authenticator is None:
            raise InvalidAuthenticationError("Authentication needs to be specified")

        self._authenticator = authenticator

    def _base_path(self) -> str:
        """
        Constructs the base path for REST API requests, differing based on whether it's an enterprise instance
        Returns:
            Base path for requests
        """
        return (
            f"{self._protocol}://{self._host}/api/v3/"
            if self._is_enterprise else
            f"{self._protocol}://{self._host}/"
        )

    def _generate_headers(self, **kwargs):
        """
        Generates headers for the request including authorization and any additional provided headers
        Args:
            **kwargs: Headers

        Returns:
            Headers required for requests
        """
        headers = {}

        headers.update(self._authenticator.get_authorization_header())
        headers.update(kwargs)

        return headers

    def get(self, path: str, **kwargs):
        """
        Makes a GET request to the specified path, handling rate limits and retrying as needed
        Args:
            path: API path to hit
            **kwargs: Arguments for the GET request

        Returns:
            Response as a JSON
        """
        path = path[1:] if path.startswith("/") else path
        kwargs.setdefault("headers", {})

        kwargs["headers"] = self._generate_headers(**kwargs["headers"])

        response = None
        json_response = None

        i = -1

        while json_response is None and i < 10:
            i += 1

            try:
                response = requests.get(
                    f"{self._base_path()}{path}", **kwargs
                )

                if int(response.headers["X-RateLimit-Remaining"]) < 2:
                    reset_at = datetime.fromtimestamp(int(response.headers["X-RateLimit-Reset"]))
                    current_time = datetime.utcnow()

                    seconds = (reset_at - current_time).total_seconds()
                    print(f"waiting for {seconds}s.")
                    time.sleep(seconds + 5)

                    json_response = None
                    continue

                if response.status_code == 202:
                    json_response = None
                    time.sleep(randint(0, i))

                    continue

                json_response = response.json()

            except RequestException:
                raise QueryFailedException(response=response)

        return json_response
