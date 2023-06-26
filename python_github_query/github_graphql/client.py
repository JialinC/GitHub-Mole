import time
from datetime import datetime
from random import randint
from string import Template
from typing import Union

import requests
from requests import Response
from requests.exceptions import RequestException
from .authentication import Authenticator
from .query import PaginatedQuery, Query


class InvalidAuthenticationError(Exception):
    pass


class QueryFailedException(Exception):
    def __init__(self, response: Response, query: str = None):
        if query:
            super().__init__(
                f"Query failed to run by returning code of {response.status_code}.\nQuery={query}\n{response.text}"
            )
        else:
            super().__init__(
                f"Query failed to run by returning code of {response.status_code}.\n"
                f"Path={response.request.path_url}\n{response.text}"
            )


class Client:
    """
    GitHub GraphQL Client.
    """
    def __init__(self,
                 protocol: str = "https",
                 host: str = "api.github.com",
                 is_enterprise: bool = False,
                 authenticator: Authenticator = None):
        """
        Initializes the client.
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

        self.rest = RESTClient(
            protocol=self._protocol, host=self._host, is_enterprise=self._is_enterprise,
            authenticator=self._authenticator
        )

    def _base_path(self):
        """
        Returns base path for a GraphQL Request.
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
        Generates headers for a request including authentication headers.
        Args:
            **kwargs: Headers

        Returns:
            Headers required for requests
        """
        headers = {}

        headers.update(self._authenticator.get_authorization_header())
        headers.update(kwargs)

        return headers

    def _execute(self, query: Union[str, Query], substitutions: dict):
        """
        Executes a query after substituting values.
        Args:
            query: Query to run
            substitutions: Substitutions to make

        Returns:
            Response as a JSON
        """
        while True:
            response = requests.post(
                self._base_path(),
                json={
                    'query': Template(query).substitute(**substitutions)
                    if isinstance(query, str) else query.substitute(**substitutions)
                },
                headers=self._generate_headers()
            )

            if int(response.headers["X-RateLimit-Remaining"]) < 2:
                reset_at = datetime.utcfromtimestamp(int(response.headers["X-RateLimit-Reset"]))
                current_time = datetime.utcnow()

                seconds = (reset_at - current_time).total_seconds()
                print(f"waiting for {seconds}s.")
                time.sleep(seconds + 5)

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
        Executes a query after substituting values. The query could be a Query or a PaginatedQuery.
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
        Executes a PaginatedQuery after substituting values.
        Args:
            query: Query to run
            substitutions: Substitutions to make

        Returns:
            Response as a JSON
        """
        while query.paginator.has_next():
            response = self._execute(query, substitutions)

            curr_info = response

            for field_name in query.path:
                curr_info = curr_info[Template(field_name).substitute(**substitutions)]

            end_cursor = curr_info["pageInfo"]["endCursor"]
            has_next_page = curr_info["pageInfo"]["hasNextPage"]

            query.paginator.update_paginator(has_next_page, end_cursor)

            yield response


class RESTClient:
    """
    Client for GitHub REST API.
    """
    def __init__(self,
                 protocol: str = "https",
                 host: str = "api.github.com",
                 is_enterprise: bool = False,
                 authenticator: Authenticator = None):
        """
        Initializes the client.
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
        Returns base path for a GraphQL Request.
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
        Generates headers for a request including authentication headers.
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
        Runs a GET request and returns a response.
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
