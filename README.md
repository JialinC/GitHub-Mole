# Students' Pre-class GitHub Contribution Research
This is a research project about students pre-class GitHub contribution and its impact on students' in-class performance.

# Python Version
We provide a convenient tool to query a user's GitHub metrics.

**IN ORDER TO USE THIS TOOL, YOU NEED TO PROVIDE YOUR OWN .env FILE.**
Because we use the [dotenv](https://pypi.org/project/python-dotenv/) package to load environment variable.
**YOU ALSO NEED TO PROVIDE YOUR GITHUB PERSONAL ACCESS TOKEN(PAT) IN YOUR .env FILE**
i.e. GITHUB_TOKEN  = 'yourGitHubPAT'

## Installation
pip -r requirements.txt
## Execution
TBD

### authentication  — Basic authenticator class
Source code: [github_graphql/authentication.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/authentication.py)

This module provides the basic authentication mechanism. User needs to provide a valid GitHub PAT with correct scope to run queries. 
A PersonalAccessTokenAuthenticator object will be created with the PAT that user provided. get_authorization_header method will return an
 authentication header that will be used when send request to GitHub GraphQL server.

<span style="font-size: larger;">Authenticator Objects</span>

Parent class of PersonalAccessTokenAuthenticator. Serve as base class of any authenticators.

<span style="font-size: larger;">PersonalAccessTokenAuthenticator Objects</span>

Handles personal access token authentication method for GitHub clients.

`class PersonalAccessTokenAuthenticator(token)`
* The `token` argument is required. This is the user's GitHub personal access token with the necessary scope to execute the queries that the user required.

Instance methods:

`get_authorization_header()`
* Returns the authentication header as a dictionary i.e. {"Authorization": "your_access_token"}.

### client  — 
Source code: [github_graphql/client.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/client.py)

This module contains

### query  — Classes for building GraphQL queries
Source code: [github_graphql/query.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/query.py)

This module provides a framework for building GraphQL queries using Python classes. The code defines four classes: QueryNode, QueryNodePaginator, Query, and PaginatedQuery.
QueryNode represents a basic building block of a GraphQL query. 
QueryNodePaginator is a specialized QueryNode for paginated requests. 
Query represents a terminal query node that can be executed. 
PaginatedQuery represents a terminal query node designed for paginated requests.

<span style="font-size: larger;">QueryNode Objects</span>

The QueryNode class  this code provides a framework for constructing GraphQL queries using Python classes. 
It allows for building complex queries with nested fields and supports pagination for paginated requests.

`class QueryNode(name, fields, args)`
* `name` is the name of the QueryNode
* `fields` is a List of fields in the QueryNode
* `args` is a Map of arguments in the QueryNode.

Private methods:

`_format_args()`
* _format_args method takes the arguments of a QueryNode instance and formats them as a string representation in the form of key-value pairs. The formatting depends on the type of the argument value, with special handling for strings, lists, dictionaries, booleans, and the default case for other types. The method then returns the formatted arguments as a string enclosed within parentheses.

`_format_fields()`
* _format_fields method takes the list of fields within a QueryNode instance and formats them as a single string representation.

Instance methods:

`get_connected_nodes()`
* get_connected_nodes method returns a list of connected QueryNode instances within a QueryNode instance. It iterates over the fields attribute of the QueryNode instance and checks if each field is an instance of QueryNode. The resulting list contains all the connected QueryNode instances found.

`__str__()`
* \__str\__ method defines how the QueryNode object should be represented as a string. It combines the object's name, formatted arguments, and formatted fields to construct the string representation in a specific format.

`__repr__()`
* Debug method.

<span style="font-size: larger;">QueryNodePaginator Objects</span>

The QueryNodePaginator class extends the QueryNode class and adds pagination-related functionality. 
It keeps track of pagination state, appends pagination fields to the existing fields, 
provides methods to check for a next page and update the pagination state, 
and includes a method to reset the pagination state.


`class QueryNodePaginator(name, fields, args, page_length)`
* `name` is the name of the QueryNode, 
* `fields` is a List of fields in the QueryNode, 
* `args` is a Map of arguments in the QueryNode, 
* `page_length` is the length of each page.

Private methods:

`_append_paginator_fields`
* _append_paginator_fields method adds pagination-related fields to the args dictionary and additional fields to the fields list of a QueryNodePaginator instance. 
It ensures that the necessary pagination fields are present in the args dictionary 
and appends "totalCount" and a QueryNode instance representing "pageInfo" with fields "hasNextPage" and "endCursor" to the list of fields.

Instance methods:

`has_next`
`update_paginator`
`reset_paginator`

<span style="font-size: larger;">Query Objects</span>

<span style="font-size: larger;">PaginatedQuery Objects</span>

### repositories  — 
Source code: [miners/repositories.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/miners/repositories.py)

### comments  — 
Source code: [queries/comments.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/comments.py)

### commits  — 
Source code: [queries/commits.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/commits.py)

### contributions  — 
Source code: [queries/contributions.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/contributions.py)

### login  — 
Source code: [queries/login.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/login.py)

### metrics  — 
Source code: [queries/metrics.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/metrics.py)

### repositories  — 
Source code: [queries/repositories.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/repositories.py)

### repositories_graph —
Source code: [queries/repositories_graph.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/repository_graph.py)