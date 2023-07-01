from string import Template
from typing import Union, List, Dict
from datetime import datetime
from collections import deque


class InvalidQueryException(Exception):
    pass


class QueryNode:
    """
    Basic building block of a Query.
    """

    def __init__(self, name: str = "query", fields: List[Union[str, 'QueryNode']] = [], args: Dict = None):
        """
        Initializes a QueryNode.
        Args:
            name: Name of the QueryNode
            fields: List of fields in the QueryNode
            args: Map of arguments in the QueryNode
        """
        self.name = name
        self.fields = fields
        self.args = args

    def _format_args(self):
        """
        Formats arguments as a string.
        Returns:
            Arguments as a string
        """
        if self.args is None:
            return ""

        args_list = []
        for key, value in self.args.items():
            if value == "$user":
                args_list.append(f'{key}: "{value}"')
            elif isinstance(value, str):
                args_list.append(f'{key}: {value}')
            elif isinstance(value, list):
                args_list.append(f'{key}: [{", ".join(value)}]')
            elif isinstance(value, dict):
                args_list.append(f'{key}: ' + "{" + ", ".join(f"{key}: {v}" for key, v in value.items()) + "}")
            elif isinstance(value, bool):
                args_list.append(f'{key}: {str(value).lower()}')
            else:
                args_list.append(f'{key}: {value}')

        return "(" + ", ".join(args_list) + ")"

    def _format_fields(self):
        """
        Formats fields as a string.
        Returns:
            Fields as a string
        """
        fields_list = [str(field) for field in self.fields]

        return " ".join(fields_list)

    def get_connected_nodes(self):
        """
        Returns all the connected QueryNodes.
        Returns:
            List of connected QueryNodes
        """
        return [field for field in self.fields if isinstance(field, QueryNode)]

    def __str__(self):
        return f"{self.name}{self._format_args()} {{ {self._format_fields()} }}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, QueryNode):
            return False

        return (
                self.name == other.name
                and self.fields == other.fields
                and self.args == other.args
        )


class Query(QueryNode):
    """
    Terminal QueryNode that can be executed.
    """
    @staticmethod
    def test_time_format(time_string: str):
        try:
            datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
            return True
        except ValueError:
            return False

    @staticmethod
    def convert_dict(data: Dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, bool):
                result[key] = str(value).lower()
            elif isinstance(value, dict):
                result[key] = "{" + ", ".join(f"{key}: {value}" for key, value in value.items()) + "}"
            elif isinstance(value, str) and Query.test_time_format(value):
                result[key] = '"' + value + '"'
            else:
                result[key] = value
        return result

    def substitute(self, **kwargs):
        """
        Substitutes Query with values.
        Args:
            **kwargs: Map of substitutions

        Returns:
            Modified Query as a string
        """
        converted_args = Query.convert_dict(kwargs)
        return Template(self.__str__()).substitute(**converted_args)


class QueryNodePaginator(QueryNode):
    """
    Specialized QueryNode for paginated requests.
    """

    def __init__(self, name: str = "query", fields: List[Union[str, 'QueryNode']] = [], args: Dict = None):
        """
        Initializes a QueryNodePaginator.
        Args:
            name: Name of the QueryNode
            fields: List of fields in the QueryNode
            args: Map of arguments in the QueryNode
        """
        super().__init__(name=name, fields=fields, args=args)
        self.has_next_page = True

    def update_paginator(self, has_next_page: bool, end_cursor: str = None):
        """
        Add end cursor to paginator arguments
        Args:
            has_next_page: has next page to update with
            end_cursor: the end cursor for pagination
        """
        self.has_next_page = has_next_page
        if end_cursor is None:
            end_cursor = ""
        self.args.update({"after": '"'+end_cursor+'"'})

    def has_next(self):
        """
        Checks if there exists a next page.
        Returns:
            Boolean if a next page exists
        """
        return self.has_next_page

    def reset_paginator(self):
        """
        Resets the QueryPaginator
        """
        self.args.pop("after")
        self.has_next_page = None

    def __eq__(self, other):
        if not isinstance(other, QueryNodePaginator):
            return False

        return super().__eq__(other)


class PaginatedQuery(Query):
    """
    Terminal QueryNode that can be executed designed for paginated requests.
    """

    def __init__(self, name: str = "query", fields: List[Union[str, 'QueryNode']] = None, args: Dict = None):
        """
        Initializes a PaginatedQuery.
        Args:
            name: Name of the QueryNode
            fields: List of fields in the QueryNode
            args: Map of arguments in the QueryNode
        """
        super().__init__(name=name, fields=fields, args=args)
        self.path, self.paginator = PaginatedQuery.extract_path_to_pageinfo_node(self)

    @staticmethod
    def extract_path_to_pageinfo_node(paginated_query: 'PaginatedQuery'):
        """
        Extract the path to the QueryNodePaginator node.
        The path is further used as index into the json object to find the pageInfo node
        Args:
            paginated_query: The PaginatedQuery to extract the path
        """
        paths = deque([([], None, paginated_query.fields)])
        while paths:
            current_path, previous_node, current_fields = paths.popleft()
            for field in current_fields:
                if isinstance(field, QueryNode):
                    if field.name == "pageInfo":
                        return current_path, previous_node
                    paths.append((current_path + [field.name], field, field.fields))
        raise InvalidQueryException("Paginator node not found")
