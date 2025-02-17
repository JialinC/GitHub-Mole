"""The module defines a client class that executes the given GraphQL query string."""

import logging
import re
import time
from datetime import datetime, timezone
from typing import Union, Optional, Dict, Any, Generator, Tuple
import requests
from requests.exceptions import Timeout, RequestException
from requests import Response
from app.services.github_query.queries.query import (
    Query,
    PaginatedQuery,
)
from app.services.github_query.queries.costs.query_cost import (
    QueryCost,
)
from .authentication import (
    Authenticator,
)

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2


class InvalidAuthenticationError(Exception):
    """Exception raised when an authentication object is invalid or not provided."""


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
            message = (
                f"Query failed with code {response.status_code}. "
                f"Query: {query}. Response: {response.text}"
            )
        else:
            message = (
                f"Query failed with code {response.status_code}. "
                f"Path: {response.request.path_url}. Response: {response.text}"
            )
        super().__init__(message)


class Client:
    """
    Client is a class that sends the given GraphQL queries to the GitHub GraphQL API and returns the query results.
    The class is responsible for constructing requests, executing them, handling errors, and managing pagination.
    It supports both public GitHub and GitHub Enterprise.
    """

    def debug_response(self, response: Response) -> None:
        print(response.json())
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")

    def __init__(
        self,
        protocol: str = "https",
        host: str = "api.github.com",
        is_enterprise: bool = False,
        authenticator: Optional[Authenticator] = None,
        retry_attempts: int = 3,
        timeout_seconds: int = 15,
    ) -> None:
        """
        Initializes the client with the necessary configuration and authentication.

        Args:
            protocol (str): The protocol to use for connecting to the GitHub server.
            host (str): The host address of the GitHub server.
            is_enterprise (bool): Indicates whether the client is connecting to a GitHub Enterprise instance.
            authenticator (Optional[Authenticator]): The authenticator instance for handling authentication.
            retry_attempts (int): The number of times to retry the request before giving up.
            timeout_seconds (int): The number of seconds to wait for a response before timing out.

        Raises:
            InvalidAuthenticationError: If no authenticator is provided or if the provided authenticator is invalid.
        """
        self._protocol = protocol
        self._host = host
        self._is_enterprise = is_enterprise
        self._retry_attempts = retry_attempts
        self._timeout_seconds = timeout_seconds

        if authenticator is None:
            raise InvalidAuthenticationError("Authentication needs to be specified")
        self._authenticator = authenticator

    def _base_path(self) -> str:
        """
        Constructs the base URL path for the GitHub GraphQL API.

        Returns:
            str: The base URL path for the GitHub GraphQL API.
        """
        return (
            f"{self._protocol}://{self._host}/graphql"
            if self._is_enterprise
            else f"{self._protocol}://{self._host}/graphql"
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

    def _retry_request(self, query: str) -> Response:
        """
        Tries to send a request multiple times until it succeeds or the retry limit is reached.

        Args:
            query (str): The GraphQL query to execute.

        Returns:
            Response: The server's response to the HTTP request.

        Raises:
            QueryFailedException: If all retry attempts fail due to API errors.
            Timeout: If all retry attempts are exhausted and the request keeps timing out.
        """
        if isinstance(query, Query):
            query = query.get_query()

        last_exception = None
        response = None

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    self._base_path(),
                    json={"query": query},
                    headers=self._generate_headers(),
                    timeout=self._timeout_seconds,
                )
                # self.debug_response(response)
                res = response.json()
                if "errors" in res and res["errors"][0]["type"] == "RATE_LIMITED":
                    current_time = datetime.now(timezone.utc)
                    reset_timestamp = int(response.headers.get("X-RateLimit-Reset"))
                    reset_at = datetime.fromtimestamp(reset_timestamp, tz=timezone.utc)
                    time_diff = reset_at - current_time
                    seconds = time_diff.total_seconds()

                    return {
                        "no_limit": True,
                        "wait_seconds": seconds + 3,
                        "reset_at": reset_at.isoformat(),
                    }

                if response.status_code == 200:
                    return response

            except Timeout as e:
                last_exception = e
                logging.warning(
                    "Request timed out. Retrying in %d seconds...",
                    INITIAL_RETRY_DELAY * (2**attempt),
                )
                time.sleep(INITIAL_RETRY_DELAY * (2**attempt))

            except RequestException as e:
                last_exception = e
                logging.error("Request failed: %s. Retrying...", str(e))
                time.sleep(INITIAL_RETRY_DELAY * (2**attempt))
        if not response:
            raise Timeout("All retry attempts exhausted.") from last_exception
        raise QueryFailedException(query=query, response=response)

    def _execute(self, query: Union[str, Query]) -> Dict[str, Any]:
        """
        Executes a query and handles response processing and error checking.

        Args:
            query (Union[str, Query]): The GraphQL query to execute.

        Returns:
            Dict[str, Any]: The parsed JSON response from the server.

        Raises:
            QueryFailedException: If the query execution fails or returns errors.
        """

        response = self._retry_request(query)
        if isinstance(response, dict) and response.get("no_limit"):
            return response
        try:
            json_response = response.json()
        except RequestException as e:
            raise QueryFailedException(query=query, response=response) from e

        if response.status_code == 200 and "errors" not in json_response:
            return json_response["data"]
        raise QueryFailedException(query=query, response=response)

    def _execution_generator(
        self, query: PaginatedQuery
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Handles the iteration over paginated query results, yielding each page's data as it's fetched.

        Args:
            query (Union[Query, PaginatedQuery]): The paginated GraphQL query to execute.

        Returns:
            Generator[Dict[str, Any], None, None]: A generator yielding each page's data as a dictionary.
        """
        while query.paginator.has_next():
            response = self._execute(query)
            curr_node = response

            for field_name in query.path:
                curr_node = curr_node[field_name]

            end_cursor = curr_node["pageInfo"]["endCursor"]
            has_next_page = curr_node["pageInfo"]["hasNextPage"]
            query.paginator.update_paginator(has_next_page, end_cursor)
            yield response

    def execute(
        self,
        query: Union[str, Query, PaginatedQuery],
        pagination: str = "backend",
        has_next_page: bool = None,
        end_cursor: str = None,
    ) -> Dict[str, Any]:
        """
        Public method to execute a non-paginated or paginated query.

        Args:
            query (Union[str, Query, PaginatedQuery]): The GraphQL query to execute.
        Returns:
            Dict[str, Any]: The parsed JSON response from the server.
        """
        if pagination == "frontend":
            if end_cursor is not None:
                query.paginator.update_paginator(True, end_cursor)
            response = self._execute(query)
            return response
        if isinstance(query, PaginatedQuery):
            return self._execution_generator(query)
        return self._execute(query)

    def _have_limit(self, query: Union[str, Query]) -> Tuple[bool, str]:
        if isinstance(query, Query):
            query = query.get_query()
        match = re.search(r"query\s*{(?P<content>.+)}", query)
        # pre-calculate the cost of the upcoming graphql query
        rate_query = QueryCost(match.group("content"), dryrun=True).get_query()
        rate_limit = self._retry_request(rate_query)
        rate_limit = rate_limit.json()["data"]["rateLimit"]
        cost, remaining, reset_at = (
            rate_limit["cost"],
            rate_limit["remaining"],
            rate_limit["resetAt"],
        )
        return (self._retry_attempts * cost > remaining, reset_at)
