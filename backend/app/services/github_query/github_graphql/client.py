import re
import time
from datetime import datetime
from random import randint
from string import Template
from typing import Union
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
    def __init__(self, response: Response, query: str = None):
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
    GitHub GraphQL Client for making GraphQL queries.
    Handles the construction and execution of queries with provided authentication.
    """
    def __init__(self, protocol: str = "https", host: str = "api.github.com", is_enterprise: bool = False, authenticator: Authenticator = None):
        """
        Initialization with protocol, host, and whether the GitHub instance is Enterprise.
        Requires an Authenticator to be provided for handling authentication.
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
        # Instantiating the RESTClient with the same configuration for REST API operations
        self.rest = RESTClient(protocol=self._protocol, host=self._host, is_enterprise=self._is_enterprise, authenticator=self._authenticator)
        
    def _base_path(self):
        """
        Constructs the base path for GraphQL requests, differing based on whether it's an enterprise instance
        Returns:
            Base path for requests
        """
        return (
            f"{self._protocol}://{self._host}/api/graphql"
            if self._is_enterprise else
            f"{self._protocol}://{self._host}/graphql"
        )

    def _generate_headers(self, **kwargs):
        """
        Generates headers for the request including authorization and any additional provided headers
        Args:
            **kwargs: Headers
        Returns:
            Headers required for requests
        """
        headers = self._authenticator.get_authorization_header()
        headers.update(kwargs)
        return headers

    def _retry_request(self, retry_attempts: int, timeout_seconds: int, query: Union[str, Query], substitutions: dict):
        """
        Attempts a request with specified retries and timeout, making substitutions into the query as needed
        If successful, returns the response, otherwise continues retrying until attempts are exhausted
        Args:
            retry_attempts: retry attempts
            timeout_seconds: timeout seconds
            query: Query to run
            substitutions: Substitutions to make
        Returns:
            Response as a JSON
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

    def _execute(self, query: Union[str, Query], substitutions: dict):
        """
        Executes a query after performing necessary substitutions
        Checks rate limits and waits if necessary before executing
        If successful, returns the data, otherwise raises QueryFailedException
        Args:
            query: Query to run
            substitutions: Substitutions to make
        Returns:
            Response as a JSON
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

    def execute(self, query: Union[str, Query, PaginatedQuery], substitutions: dict):
        """
        Public method to execute a given query, handling pagination if necessary
        Args:
            query: Query to run
            substitutions: Substitutions to make
        Returns:
            Response as a JSON
        """
        if isinstance(query, PaginatedQuery):
            return self._execution_generator(query, substitutions)

        return self._execute(query, substitutions)

    def _execution_generator(self, query, substitutions: dict):
        """
        Handles execution of paginated queries, yielding results as they are available
        Args:
            query: Query to run
            substitutions: Substitutions to make
        Returns:
            Response as a JSON
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
    def __init__(self, protocol: str = "https", host: str = "api.github.com", is_enterprise: bool = False, authenticator: Authenticator = None):
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

    def _base_path(self):
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
