from python_github_query.github_graphql.query import QueryNode, Query, QueryNodePaginator, PaginatedQuery


class TestQuery:
    def test_query_node_format_args(self):
        node = QueryNode(args={"arg1": "value1",
                               "arg2": ["value2", "value3"],
                               "arg3": {"nested": "value4"},
                               "arg4": True,
                               "arg5": 1,
                               "arg6": "$pg_size"})

        formatted_args = node._format_args()
        expected_args = '(arg1: "value1", arg2: [value2, value3], arg3: {nested: value4}, ' \
                        'arg4: true, arg5: 1, arg6: $pg_size)'
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
        paginator = QueryNodePaginator(name="query", fields=["field1", "field2"], args={"arg1": "value1"})
        assert paginator.name == "query"
        assert paginator.fields == ["field1", "field2"]
        assert paginator.args == {"arg1": "value1"}
        assert paginator.has_next_page is True

    def test_query_node_paginator_update_paginator(self):
        paginator = QueryNodePaginator(name="query", fields=["field1"], args={"arg1": "value1"})
        paginator.update_paginator(has_next_page=False, end_cursor="abc123")

        assert paginator.has_next_page is False
        assert paginator.args["after"] == "abc123"

    def test_query_node_paginator_has_next(self):
        paginator = QueryNodePaginator()
        assert paginator.has_next() is True

        paginator.has_next_page = False
        assert paginator.has_next() is False

    def test_query_node_paginator_reset_paginator(self):
        paginator = QueryNodePaginator(name="query", fields=["field1"], args={"arg1": "value1"})
        paginator.has_next_page = False
        paginator.args["after"] = "abc123"
        paginator.reset_paginator()

        expected_args = {"arg1": "value1"}
        assert paginator.args == expected_args
        assert paginator.has_next_page is None

    def test_query_node_paginator_equality(self):
        paginator1 = QueryNodePaginator(name="query", fields=["field1"], args={"arg1": "value1"})
        paginator2 = QueryNodePaginator(name="query", fields=["field1"], args={"arg1": "value1"})
        paginator3 = QueryNodePaginator(name="query", fields=["field2"], args={"arg1": "value1"})

        assert paginator1 == paginator2
        assert paginator1 != paginator3

    def test_paginated_query_initialization(self):
        fields = [
            QueryNode("user", fields=[
                "login",
                "name",
                QueryNode("repository",
                          fields=[
                              QueryNode("pageInfo",
                                        fields=[
                                            "endCursor",
                                            "hasNextPage"]
                                        )
                              ]
                          )
                ]
            )
        ]

        query = PaginatedQuery(name="query", fields=fields)

        expected_path = ["user", "repository"]
        expected_paginator = fields[0].fields[2]

        assert query.name == "query"
        assert query.fields == fields
        assert query.args is None
        assert query.path == expected_path
        assert query.paginator == expected_paginator

    def test_extract_path_to_pageinfo_node(self):
        fields = [
            QueryNode("user", fields=["login", "name"]),
            QueryNode("repository", fields=[
                QueryNode("pageInfo", fields=["endCursor", "hasNextPage"])
            ])
        ]

        query = PaginatedQuery(name="query", fields=fields)
        path, paginator = PaginatedQuery.extract_path_to_pageinfo_node(query)
        expected_path = ["repository"]
        expected_paginator = query.fields[1]
        assert path == expected_path
        assert paginator == expected_paginator

