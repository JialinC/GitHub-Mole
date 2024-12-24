"""The module defines four query-related classes that are used to generate GraphQL query strings
in an object-oriented way."""

from typing import Union, List, Dict, Tuple, Optional
from datetime import datetime
from collections import deque


class InvalidQueryException(Exception):
    """
    Exception raised for errors in the GraphQL query. This can be due to an invalid query structure,
    incorrect execution parameters, or other issues that make the query invalid.

    Attributes:
        message (str): Explanation of the error.
        Provides more details about what part of the query or its execution is considered invalid.
    """

    def __init__(
        self, message: str = "Invalid query structure or execution parameters"
    ) -> None:
        """
        Initializes the InvalidQueryException with an error message.

        Args:
            message (str): A human-readable string explaining the error. Defaults to a general message about invalid
            query structure or parameters.
        """
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Returns a string representation of the exception, typically the error message.

        Returns:
            str: The string representation of the exception.
        """
        return f"{self.__class__.__name__}: {self.message}"


class QueryNode:
    """
    QueryNode is the fundamental building block of a GraphQL query.It represents a field or a set of fields,
    along with any associated arguments, that can be requested from the GraphQL API.
    QueryNodes can be nested, allowing for the representation of complex queries.
    """

    def __init__(
        self,
        name: str = "query",
        fields: List[Union[str, "QueryNode"]] = None,
        args: Dict = None,
    ) -> None:
        """
        Initializes a QueryNode with a name, a list of fields, and optional arguments.

        Args:
            name (str): The name of the QueryNode, typically representing a field or operation in the GraphQL query.
            fields (List[Union[str, 'QueryNode']]): A list of fields to include in the QueryNode.
            These can be strings representing field names or other nested QueryNodes.
            args (Dict): A dictionary of arguments to include with the QueryNode.
            These are used to parameterize the query and provide variables for the fields requested.
        """
        self.name = name
        if fields is None:
            self.fields = []
        else:
            self.fields = fields
        self.args = args

    def _format_args(self) -> str:
        """
        Formats the arguments of the QueryNode into a string suitable for inclusion in a GraphQL query.
        This involves converting each argument into the appropriate query syntax.

        Returns:
            str: A string representation of the arguments, formatted for a GraphQL query.
        """
        if self.args is None:
            return ""

        args_list = []
        for key, value in self.args.items():
            if key == "login":
                args_list.append(f'{key}: "{value}"')
            elif key == "owner":
                args_list.append(f'{key}: "{value}"')
            elif key == "name":
                args_list.append(f'{key}: "{value}"')
            elif isinstance(value, list):
                args_list.append(f'{key}: [{", ".join(value)}]')
            elif isinstance(value, dict):
                args_list.append(
                    f"{key}: "
                    + "{"
                    + ", ".join(f"{key}: {v}" for key, v in value.items())
                    + "}"
                )
            elif isinstance(value, bool):
                args_list.append(f"{key}: {str(value).lower()}")
            else:
                args_list.append(f"{key}: {value}")

        return "(" + ", ".join(args_list) + ")"

    def _format_fields(self) -> str:
        """
        Formats the fields of the QueryNode into a string suitable for inclusion in a GraphQL query.
        This involves converting each field and any nested QueryNodes into the appropriate query syntax.

        Returns:
            str: A string representation of the fields, formatted for a GraphQL query.
        """
        fields_list = [str(field) for field in self.fields]

        return " ".join(fields_list)

    def get_connected_nodes(self) -> List["QueryNode"]:
        """
        Retrieves all connected QueryNodes within this QueryNode.
        This method is useful for traversing analyzing a complex query structure.

        Returns:
            List[QueryNode]: A list of all directly connected QueryNodes within this QueryNode.
        """
        return [field for field in self.fields if isinstance(field, QueryNode)]

    def get_query(self) -> str:
        """
        Returns the query string representation of the QueryNode.

        Returns:
            str: The query string representation of the QueryNode.
        """
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name}{self._format_args()} {{ {self._format_fields()} }}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: "QueryNode") -> bool:
        """
        Compares this QueryNode with another to determine if they are equivalent.
        """
        return (
            isinstance(other, QueryNode)
            and self.name == other.name
            and self.fields == other.fields
            and self.args == other.args
        )


class Query(QueryNode):
    """
    Query is a subclass of QueryNode specifically designed to represent a complete, executable GraphQL query.
    It provides additional functionality for formatting and substituting values in preparation for execution.
    """

    @staticmethod
    def test_time_format(time_string: str) -> bool:
        """
        Checks if the given string matches the expected time format ("%Y-%m-%dT%H:%M:%SZ").

        Args:
            time_string (str): The time string to be tested.

        Returns:
            bool: True if the string matches the time format, False otherwise.
        """
        try:
            datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
            return True
        except ValueError:
            return False


class QueryNodePaginator(QueryNode):
    """
    QueryNodePaginator is a specialized version of QueryNode designed specifically for paginated requests.
    It includes functionality to manage and track the state of pagination through GraphQL queries.
    """

    def __init__(
        self,
        name: str = "query",
        fields: List[Union[str, "QueryNode"]] = None,
        args: Dict[str, str] = None,
    ) -> None:
        """
        Initializes a QueryNodePaginator with name, fields, and arguments, setting up the initial state for pagination.

        Args:
            name (str): Name of the QueryNodePaginator, typically representing a field in the GraphQL query.
            fields (List[Union[str, 'QueryNode']]): A list of fields or nested QueryNodes that the paginator
            will handle.
            args (Dict): A dictionary of arguments relevant to pagination, such as 'first', 'after', etc.
        """
        if fields is None:
            fields = []
        if args is None:
            args = {}
        super().__init__(name=name, fields=fields, args=args)
        self.has_next_page = True

    def update_paginator(
        self, has_next_page: bool, end_cursor: Optional[str] = None
    ) -> None:
        """
        Updates the pagination state with information about the next page and the end cursor.

        Args:
            has_next_page (bool): Indicates whether there is a next page available.
            end_cursor (str, optional): The cursor that should be used to fetch the next page. Defaults to None.
        """
        self.has_next_page = has_next_page
        if end_cursor is None:
            end_cursor = ""
        self.args.update({"after": '"' + end_cursor + '"'})

    def has_next(self) -> bool:
        """
        Checks whether there is a next page available based on the current pagination state.

        Returns:
            bool: True if there is another page to be fetched, False otherwise.
        """
        return self.has_next_page

    def reset_paginator(self) -> None:
        """
        Resets the pagination state, typically used when restarting or reinitializing the pagination process.
        """
        self.args.pop("after")
        self.has_next_page = None

    def __eq__(self, other: "QueryNodePaginator") -> bool:
        """
        Compares this QueryNodePaginator with another to determine if they are equivalent in terms of their name,
        fields, arguments, and pagination state.

        Args:
            other: Another QueryNodePaginator object to compare against.

        Returns:
            bool: True if both have the same name, fields, arguments, and pagination state; False otherwise.
        """
        return isinstance(other, QueryNodePaginator) and super().__eq__(other)


class PaginatedQuery(Query):
    """
    PaginatedQuery is a subclass of Query specifically designed to handle paginated GraphQL queries.
    It provides methods to manage and extract information related to pagination, such as pageInfo
    and navigation through pages.
    """

    def __init__(
        self,
        name: str = "query",
        fields: Optional[List[Union[str, "QueryNode"]]] = None,
        args: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initializes a PaginatedQuery with a name, a list of fields, and optional arguments,
        setting up for handling paginated data.

        Args:
            name (str): Name of the PaginatedQuery, typically representing the operation in the GraphQL query.
            fields (List[Union[str, 'QueryNode']]): A list of fields or nested QueryNodes that the query will include.
            args (Dict): A dictionary of arguments relevant to the query, not specifically to pagination.
        """
        super().__init__(name=name, fields=fields, args=args)
        self.path, self.paginator = PaginatedQuery.extract_path_to_pageinfo_node(self)

    @staticmethod
    def extract_path_to_pageinfo_node(
        paginated_query: "PaginatedQuery",
    ) -> Tuple[List[str], Optional["QueryNodePaginator"]]:
        """
        Extracts the path to the pageInfo node within the structure of the paginated query.
        This path is used to navigate through the nested structure of the query's response to find and
        update pagination-related information.

        Args:
            paginated_query (PaginatedQuery): The PaginatedQuery object from which to extract the path.

        Returns:
            Tuple[List[str], QueryNode]: A tuple containing the path (as a list of strings indicating field names)
            to the pageInfo node and the
            QueryNodePaginator instance associated with it.

        Raises:
            InvalidQueryException: If a paginator node or pageInfo field cannot be found in the query structure.
        """
        paths = deque([([], None, paginated_query.fields)])
        while paths:
            current_path, previous_node, current_fields = paths.popleft()
            for field in current_fields:
                if isinstance(field, QueryNode):
                    if field.name == "pageInfo":
                        return current_path, previous_node
                    if "..." in field.name:
                        paths.append((current_path, field, field.fields))
                    else:
                        paths.append((current_path + [field.name], field, field.fields))
        raise InvalidQueryException("Paginator node not found")
