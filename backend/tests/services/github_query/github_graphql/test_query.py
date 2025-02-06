from backend.app.services.github_query.github_graphql.query import QueryNode, Query, QueryNodePaginator, PaginatedQuery

class TestQueryNode:
    def test_initialization(self):
        """Test the proper initialization of a QueryNode."""
        node = QueryNode(name="testNode", fields=["field1", QueryNode(name="nestedNode")], args={"arg1": "value1"})
        assert node.name == "testNode", "The name should be initialized correctly."
        assert node.fields == ["field1", QueryNode(name="nestedNode")], "The fields should be initialized correctly."
        assert node.args == {"arg1": "value1"}, "The args should be initialized correctly."
    
    def test_format_args(self):
        """Test the _format_args method for various scenarios, including special keys and dictionary values."""
        # No args
        node_no_args = QueryNode(name="testNode")
        assert node_no_args._format_args() == "", "No args should return an empty string."

        # With basic args string, int, boolen
        node_with_args = QueryNode(name="testNode", args={"arg1": "value1", "arg2": 123, "arg3": True})
        assert node_with_args._format_args() == "(arg1: value1, arg2: 123, arg3: true)", "Args should be formatted correctly."

        # With special keys like "login", "owner", "name"
        special_key_args = QueryNode(name="testNode", args={"login": "userLogin", "owner": "userOwner", "name": "userName"})
        assert special_key_args._format_args() == '(login: "userLogin", owner: "userOwner", name: "userName")', "Special keys should be formatted correctly with quotes."

        # With list args
        list_args = QueryNode(name="testNode", args={"listArg": ["item1", "item2", "item3"]})
        assert list_args._format_args() == "(listArg: [item1, item2, item3])", "List arguments should be formatted correctly."

        # With dictionary args
        dict_args = QueryNode(name="testNode", args={"dictArg": {"key1": "value1", "key2": "value2"}})
        assert dict_args._format_args() == "(dictArg: {key1: value1, key2: value2})", "Dictionary arguments should be formatted correctly."

    def test_format_fields(self):
        """Test the _format_fields method with simple fields and nested QueryNodes."""
        # Test with simple string fields
        simple_node = QueryNode(name="testNode", fields=["field1", "field2"])
        assert simple_node._format_fields() == "field1 field2", "Simple fields should be formatted as a space-separated string."

        # Test with a nested QueryNode
        nested_node = QueryNode(name="nestedNode", fields=["nestedField1", "nestedField2"])
        parent_node = QueryNode(name="parentNode", fields=["field1", nested_node])
        expected_str = "field1 nestedNode { nestedField1 nestedField2 }"
        assert parent_node._format_fields() == expected_str, "Nested QueryNodes should be formatted correctly within fields."
    
    def test_get_connected_nodes(self):
        """Test the get_connected_nodes method to ensure it only returns nested QueryNodes."""
        # Create nested QueryNodes
        nested_node1 = QueryNode(name="nestedNode1", fields=["nestedField1", "nestedField2"])
        nested_node2 = QueryNode(name="nestedNode2", fields=["nestedField3", "nestedField4"])

        # Create parent QueryNode with a mix of string fields and nested QueryNodes
        parent_node = QueryNode(name="parentNode", fields=["field1", nested_node1, "field2", nested_node2])

        # Get connected nodes
        connected_nodes = parent_node.get_connected_nodes()

        # Check that the method returns only the nested QueryNodes
        assert connected_nodes == [nested_node1, nested_node2], "Should return only nested QueryNodes."

    def test_string_representation(self):
        """Test the string representation of QueryNode."""
        node = QueryNode(name="testNode", fields=["field1", QueryNode(name="nestedNode")], args={"arg1": "value1"})
        expected_representation = "testNode(arg1: value1) { field1 nestedNode {  } }"
        assert str(node) == expected_representation, "String representation should match the expected format."

    def test_query_node_equality(self):
        """Test the __eq__ method for QueryNode."""
        node1 = QueryNode(name="testNode", fields=["field1", "field2"], args={"arg1": "value1"})
        node2 = QueryNode(name="testNode", fields=["field1", "field2"], args={"arg1": "value1"})
        node3 = QueryNode(name="testNode", fields=["field1"], args={"arg1": "value1"})
        assert node1 == node2, "Nodes with the same content should be equal."
        assert node1 != node3, "Nodes with different content should not be equal."

class TestQuery:
    def test_query_initialization(self):
        """Test the proper initialization of a Query."""
        query = Query(name="testQuery", fields=["field1", QueryNode(name="nestedNode")], args={"arg1": "value1"})
        assert query.name == "testQuery", "The name should be initialized correctly."
        assert query.fields == ["field1", QueryNode(name="nestedNode")], "The fields should be initialized correctly."
        assert query.args == {"arg1": "value1"}, "The args should be initialized correctly."

    def test_time_format(self):
        """Test the time formatting utility method."""
        valid_time = "2020-01-01T12:00:00Z"
        invalid_time = "Not a real time"
        assert Query.test_time_format(valid_time) == True, "Should return True for valid time format."
        assert Query.test_time_format(invalid_time) == False, "Should return False for invalid time format."

    def test_convert_dict(self):
        """Test the convert_dict static method."""
        data = {
            "boolean": True,
            "dict": {"key": "value"},
            "normal": "normalValue",
            "time": "2020-01-01T12:00:00Z"
        }
        converted = Query.convert_dict(data)
        expected = {
            "boolean": "true",
            "dict": '{key: "value"}',
            "normal": "normalValue",
            "time": '"2020-01-01T12:00:00Z"'
        }
        assert converted == expected, "Should convert dictionary values appropriately."

    def test_substitute(self):
        """Test the substitute method."""
        query = Query(name="testQuery", fields=["field1"], args={"arg1": "$value"})
        substituted_query = query.substitute(value="substitutedValue")
        expected = "testQuery(arg1: substitutedValue) { field1 }"
        assert substituted_query == expected, "Should substitute values correctly into the query."

class TestQueryNodePaginator:
    def test_initialization(self):
        """Test the proper initialization of a QueryNodePaginator."""
        paginator = QueryNodePaginator(name="testPaginator", fields=["field1"], args={"arg1": "value1"})
        assert paginator.name == "testPaginator", "The name should be initialized correctly."
        assert paginator.fields == ["field1"], "The fields should be initialized correctly."
        assert paginator.args == {"arg1": "value1"}, "The args should be initialized correctly."
        assert paginator.has_next_page == True, "has_next_page should be initialized to True."

    def test_update_paginator(self):
        """Test the update_paginator method."""
        paginator = QueryNodePaginator(name="testPaginator")
        assert paginator.has_next_page == True, "Initial state should be True for has_next_page."

        # Update the paginator to reflect new pagination state
        paginator.update_paginator(has_next_page=False, end_cursor="cursor123")
        assert paginator.has_next_page == False, "has_next_page should be updated correctly."
        assert paginator.args.get("after") == '"cursor123"', "End cursor should be updated correctly."

    def test_reset_paginator(self):
        """Test the reset_paginator method."""
        paginator = QueryNodePaginator(name="testPaginator", args={"after": '"cursor123"'})
        paginator.update_paginator(has_next_page=False, end_cursor="newCursor")
        paginator.reset_paginator()

        # After resetting, "after" should be removed and has_next_page set back to None
        assert "after" not in paginator.args, "'after' should be removed from args."
        assert paginator.has_next_page == None, "has_next_page should be reset to None."

    def test_has_next(self):
        """Test the has_next method."""
        paginator = QueryNodePaginator()
        assert paginator.has_next() == True, "Initially, has_next should return True."

        paginator.update_paginator(has_next_page=False)
        assert paginator.has_next() == False, "After update, has_next should reflect the new state."

class TestPaginatedQuery:
    def test_paginated_query_initialization(self):
        """Test the proper initialization of a PaginatedQuery."""
        # Creating a mock PaginatedQuery with nested QueryNode that includes a pageInfo field
        page_info_node = QueryNode(name="pageInfo", fields=["endCursor", "hasNextPage"])
        nested_node = QueryNode(name="nestedNode", fields=[page_info_node])
        paginated_query = PaginatedQuery(name="testPaginatedQuery", fields=["field1", nested_node], args={"arg1": "value1"})

        # Asserting basic initialization
        assert paginated_query.name == "testPaginatedQuery", "The name should be initialized correctly."
        assert paginated_query.fields == ["field1", nested_node], "The fields should be initialized correctly, including the nested node."
        assert paginated_query.args == {"arg1": "value1"}, "The args should be initialized correctly."

        assert paginated_query.path == ["nestedNode"], "The path should lead to the nestedNode containing pageInfo."
        assert paginated_query.paginator == nested_node, "The paginator should be the nestedNode containing pageInfo."

    def test_extract_path_to_pageinfo_node(self):
        """Test the extract_path_to_pageinfo_node method."""
        # Creating a mock PaginatedQuery with nested QueryNode that includes a pageInfo field
        page_info_node = QueryNode(name="pageInfo", fields=["endCursor", "hasNextPage"])
        nested_node = QueryNode(name="nestedNode", fields=[page_info_node])
        paginated_query = PaginatedQuery(name="testPaginatedQuery", fields=[nested_node])

        path, paginator = paginated_query.extract_path_to_pageinfo_node(paginated_query)
        assert path == ["nestedNode"], "The path should lead to the nestedNode containing pageInfo."
        assert paginator == nested_node, "The paginator should be the nested node containing pageInfo."
