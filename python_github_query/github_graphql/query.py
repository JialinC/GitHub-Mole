from string import Template
from typing import Union, List, Dict


class InvalidQueryException(Exception):
    pass


class QueryNode:
    """
    Basic building block of a Query.
    """
    def __init__(self, name: str = "query", fields: List[Union[str, 'QueryNode']] = None, args: Dict = None):
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
            if isinstance(value, str):
                args_list.append(f'{key}: "{value}"')
            elif isinstance(value, list):
                args_list.append(f'{key}: [{", ".join(value)}]')
            elif isinstance(value, dict):
                args_list.append(f'{key}: {{{", ".join([f"{_k}:{_v}" for _k, _v in value.items()])}}}')
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


class Query(QueryNode):
    """
    Terminal QueryNode that can be executed.
    """
    def substitute(self, **kwargs):
        """
        Substitutes Query with values.
        Args:
            **kwargs: Map of substitutions

        Returns:
            Modified Query as a string
        """
        return Template(self.__str__()).substitute(**kwargs)


class QueryNodePaginator(QueryNode):
    """
    Specialized QueryNode for paginated requests.
    """
    _has_next_page = True
    _end_cursor = None

    def __init__(self, name: str = "query", fields: List[Union[str, 'QueryNode']] = None, args: Dict = None,
                 page_length: int = 100):
        """
        Initializes a QueryNodePaginator.
        Args:
            name: Name of the QueryNode
            fields: List of fields in the QueryNode
            args: Map of arguments in the QueryNode
            page_length: Length of each page
        """
        super().__init__(name=name, fields=fields, args=args)

        self.page_length = page_length
        self._append_paginator_fields()

    def _append_paginator_fields(self):
        """
        Appends paginator fields to the existing fields.
        """
        if self.args is None:
            self.args = {}

        self.args.update({"first": self.page_length})

        if self._end_cursor is not None:
            self.args.update({"after": self._end_cursor})

        self.fields.append("totalCount")
        self.fields.append(QueryNode("pageInfo", fields=["hasNextPage", "endCursor"]))

    def has_next(self):
        """
        Checks if there exists a next page.
        Returns:
            Boolean if a next page exists
        """
        return self._has_next_page

    def update_paginator(self, has_next_page: bool, end_cursor: str):
        """
        Updates QueryPaginator with new end cursor.
        Args:
            has_next_page: has_next_page to update with
            end_cursor: end_cursor to update with
        """
        self._has_next_page = has_next_page
        self._end_cursor = end_cursor

        self.args.update({"after": self._end_cursor})

    def reset_paginator(self):
        """
        Resets the QueryPaginator
        """
        self.args.pop("after")

        self._has_next_page = None
        self._end_cursor = None

class PaginatedQuery(Query):
    """
    Terminal QueryNode that can be executed designed for paginated requests.
    """
    path: List[str] = None
    paginator: QueryNodePaginator = None

    def __init__(self, name: str = "query", fields: List[Union[str, 'QueryNode']] = None, args: Dict = None):
        """
        Initializes a PaginatedQuery.
        Args:
            name: Name of the QueryNode
            fields: List of fields in the QueryNode
            args: Map of arguments in the QueryNode
        """
        super().__init__(name=name, fields=fields, args=args)

        self.path, self.paginator = PaginatedQuery.get_path_to_paginator(self)
        self.path.pop(0)

        if self.paginator is None:
            raise InvalidQueryException("Paginator node not found")

    @staticmethod
    def get_path_to_paginator(node: QueryNode):
        """
        Returns path to the PaginatedQueryNode in the PaginatedQuery.
        Args:
            node: QueryNode to start the path from

        Returns:
            Path as a list and the PaginatedQueryNode
        """
        path, paginator = [], None

        for field in node.get_connected_nodes():
            if isinstance(field, QueryNodePaginator):
                path, paginator = [field.name, ], field
            elif isinstance(field, QueryNode):
                path, paginator = PaginatedQuery.get_path_to_paginator(field)

            if paginator is not None:
                return [node.name, ] + path, paginator

        return [], None
