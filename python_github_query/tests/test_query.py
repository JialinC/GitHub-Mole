import pytest
from python_github_query.github_graphql.query import QueryNode, Query, QueryNodePaginator, PaginatedQuery


class TestQuery:
    def test_query_node_format_args(self):
        node = QueryNode(args={"arg1": "value1",
                               "arg2": ["value2", "value3"],
                               "arg3": {"nested": "value4"},
                               "arg4": True,
                               "arg5": 1})

        formatted_args = node._format_args()
        expected_args = '(arg1: "value1", arg2: [value2, value3], arg3: {nested: value4}, arg4: true, arg5: 1)'
        assert formatted_args == expected_args

    def test_query_node_format_fields(self):
        node = QueryNode(fields=["field1",
                                 "field2",
                                 QueryNode(name="nested_query",
                                           fields=["nested_field1",
                                                   "nested_field2"])])

        formatted_fields = node._format_fields()
        expected_fields = 'field1 field2 nested_query { nested_field1 nested_field2 }'
        assert formatted_fields == expected_fields

    def test_query_node_get_connected_nodes(self):
        nested_query = QueryNode(name="nested_query",
                                 fields=["nested_field1",
                                         "nested_field2"])
        node = QueryNode(name="example_query",
                         fields=["field1",
                                 "field2",
                                 nested_query])
        connected_nodes = node.get_connected_nodes()
        expected_nodes = [nested_query]
        assert connected_nodes == expected_nodes

    def test_query_node(self):
        node = QueryNode(name="example_query",
                         fields=["field1",
                                 "field2"],
                         args={"arg1": "value1",
                               "arg2": True,
                               "arg3": 1})

        assert node.name == "example_query"
        assert node.fields == ["field1", "field2"]
        assert node.args == {"arg1": "value1", "arg2": True, "arg3": 1}
        expected_str = 'example_query(arg1: "value1", arg2: true, arg3: 1) { field1 field2 }'
        assert str(node) == expected_str

    def test_query_substitute(self):
        query = Query(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        "name",
                    ]
                )
            ]
        )

        substitutions = {
            "user": "JohnDoe"
        }

        expected_substituted_query = 'query { user(login: "JohnDoe") { login name } }'
        substituted_query = query.substitute(**substitutions)

        assert substituted_query == expected_substituted_query

    def test_query_node_paginator_initialization(self):
        page_length = 50
        paginator = QueryNodePaginator(name="query", fields=["field1", "field2"], args={"arg1": "value1"},
                                       page_length=page_length)

        assert paginator.name == "query"
        assert paginator.fields == ["field1", "field2", QueryNode("pageInfo", fields=["hasNextPage", "endCursor"])]
        assert paginator.args == {"arg1": "value1", "first": page_length}
        assert paginator.page_length == page_length
        assert paginator._has_next_page is True
        assert paginator._end_cursor is None

    def test_query_node_paginator_has_next(self):
        paginator = QueryNodePaginator()
        assert paginator.has_next() is True

        paginator._has_next_page = False
        assert paginator.has_next() is False

    def test_query_node_paginator_update_paginator(self):
        paginator = QueryNodePaginator()
        paginator.update_paginator(has_next_page=False, end_cursor="abc123")

        assert paginator._has_next_page is False
        assert paginator._end_cursor == "abc123"
        assert paginator.args["after"] == "abc123"

    def test_query_node_paginator_reset_paginator(self):
        paginator = QueryNodePaginator(name="query", fields=["field1"], args={"arg1": "value1"}, page_length=50)
        paginator.update_paginator(has_next_page=True, end_cursor="abc123")
        paginator.reset_paginator()

        expected_fields = ["field1", QueryNode("pageInfo", fields=["hasNextPage", "endCursor"])]
        assert paginator.fields == expected_fields

        expected_args = {"arg1": "value1", "first": 50}
        assert paginator.args == expected_args
        assert paginator._has_next_page is None
        assert paginator._end_cursor is None

    def test_paginated_query_initialization():
        fields = [
            QueryNode("user", fields=["login", "name"]),
            QueryNodePaginator(page_length=50)
        ]

        query = PaginatedQuery(name="query", fields=fields)

        expected_path = ["query", "user"]
        expected_paginator = QueryNodePaginator(page_length=50)

        assert query.name == "query"
        assert query.fields == fields
        assert query.args is None
        assert query.path == expected_path
        assert query.paginator == expected_paginator

    def test_paginated_query_initialization_no_paginator():
        fields = [
            QueryNode("user", fields=["login", "name"]),
        ]

        with pytest.raises(InvalidQueryException):
            query = PaginatedQuery(name="query", fields=fields)

    # def test_paginated_query_get_path_to_paginator():
    #     node1 = QueryNode("user", fields=["login"])
    #     node2 = QueryNodePaginator(page_length=50)
    #     node3 = QueryNode("repository", fields=["name"])
    #
    #     node1.fields.append(node2)
    #     node2.fields.append(node3)
    #
    #     path, paginator = PaginatedQuery.get_path_to_paginator(node1)
    #     expected_path = ["user"]
    #     expected_paginator = node2
    #
    #     assert path == expected_path
    #     assert paginator == expected_paginator
    #
    # def test_paginated_query_get_path_to_paginator_no_paginator():
    #     node1 = QueryNode("user", fields=["login"])
    #     node2 = QueryNode("repository", fields=["name"])
    #
    #     node1.fields.append(node2)
    #
    #     path, paginator = PaginatedQuery.get_path_to_paginator(node1)
    #     expected_path = []
    #     expected_paginator = None
    #
    #     assert path == expected_path
    #     assert paginator == expected_paginator


