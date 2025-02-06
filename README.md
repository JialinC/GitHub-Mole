# Students' Pre-class GitHub Contribution Research

This is a research project about students pre-class GitHub contribution and its impact on students' in-class performance.

# Python Version

We provide a convenient tool to query a user's GitHub metrics.

**IN ORDER TO USE THIS TOOL, YOU NEED TO PROVIDE YOUR OWN .env FILE.**
Because we use the [dotenv](https://pypi.org/project/python-dotenv/) package to load environment variable.
**YOU ALSO NEED TO PROVIDE YOUR GITHUB PERSONAL ACCESS TOKEN(PAT) IN YOUR .env FILE**
i.e. GITHUB_TOKEN = 'yourGitHubPAT'

## Installation

We recommend using virtual environment.

```shell
cd path/to/your/project/directory
python -m venv venv
```

On macOS and Linux:

```shell
source venv/bin/activate
```

On Windows (Command Prompt):

```shell
.\venv\Scripts\activate
```

On Windows (PowerShell):

```shell
.\venv\Scripts\Activate.ps1
```

then you can

```shell
pip -r requirements.txt
```

## Execution

TBD

### authentication — Basic authenticator class

Source code: [github_graphql/authentication.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/authentication.py)

This module provides the basic authentication mechanism. User needs to provide a valid GitHub PAT with correct scope to run queries.
A PersonalAccessTokenAuthenticator object will be created with the PAT that user provided. get_authorization_header method will return an
authentication header that will be used when send request to GitHub GraphQL server.

<span style="font-size: larger;">Authenticator Objects</span>

Parent class of PersonalAccessTokenAuthenticator. Serve as base class of any authenticators.

<span style="font-size: larger;">PersonalAccessTokenAuthenticator Objects</span>

Handles personal access token authentication method for GitHub clients.

`class PersonalAccessTokenAuthenticator(token)`

- The `token` argument is required. This is the user's GitHub personal access token with the necessary scope to execute the queries that the user required.

Instance methods:

`get_authorization_header()`

- Returns the authentication header as a dictionary i.e. {"Authorization": "your_access_token"}.

### query — Classes for building GraphQL queries

Source code: [github_graphql/query.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/query.py)

This module provides a framework for building GraphQL queries using Python classes. The code defines four classes: QueryNode, QueryNodePaginator, Query, and PaginatedQuery.
QueryNode represents a basic building block of a GraphQL query.
QueryNodePaginator is a specialized QueryNode for paginated requests.
Query represents a terminal query node that can be executed.
PaginatedQuery represents a terminal query node designed for paginated requests.

- You can find more information about GitHub GraphQL API here: [GitHub GraphQL API documentation](https://docs.github.com/en/graphql)
- You can use GitHub GraphQL Explorer to try out queries: [GitHub GraphQL API Explorer](https://docs.github.com/en/graphql/overview/explorer)

<span style="font-size: larger;">QueryNode Objects</span>

The QueryNode class provides a framework for constructing GraphQL queries using Python classes.
It allows for building complex queries with nested fields and supports pagination for paginated requests.

`class QueryNode(name, fields, args)`

- `name` is the name of the QueryNode
- `fields` is a List of fields in the QueryNode
- `args` is a Map of arguments in the QueryNode.

Private methods:

`_format_args()`

- \_format_args method takes the arguments of a QueryNode instance and formats them as a string representation in the form of key-value pairs. The formatting depends on the type of the argument value, with special handling for strings, lists, dictionaries, booleans, and the default case for other types. The method then returns the formatted arguments as a string enclosed within parentheses.

`_format_fields()`

- \_format_fields method takes the list of fields within a QueryNode instance and formats them as a single string representation.

Instance methods:

`get_connected_nodes()`

- get_connected_nodes method returns a list of connected QueryNode instances within a QueryNode instance. It iterates over the fields attribute of the QueryNode instance and checks if each field is an instance of QueryNode. The resulting list contains all the connected QueryNode instances found.

`__str__()`

- \_\_str\_\_ method defines how the QueryNode object should be represented as a string. It combines the object's name, formatted arguments, and formatted fields to construct the string representation in a specific format.

`__repr__()`

- Debug method.

`__eq__(other)`

- \_\_eq\_\_ method defines how the QueryNode object should be compared to each other.

<span style="font-size: larger;">Query Objects</span>

The Query class is a subclass of QueryNode and represents a terminal QueryNode that can be executed.
It provides a substitute method to substitute values in the query using keyword arguments.

Class methods:

`test_time_format(time_string)`

- test_time_format is a static method that validates whether a given time string is in the expected format "%Y-%m-%dT%H:%M:%SZ".

`convert_dict(data)`

- convert_dict is a static method that takes a dictionary (data) as input and returns a modified dictionary with certain value conversions.
- If the value is of type bool, it converts it to a lowercase string representation.
- If the value is a nested dictionary, it converts it to a string representation enclosed in curly braces.
- If the value is a string and passes the test_time_format check, it wraps it in double quotes.
- For other value types, it keeps the value unchanged.

Instance methods:

`substitute(**kwargs)`

- This method substitutes the placeholders in the query string with specific values provided as keyword arguments.

<span style="font-size: larger;">QueryNodePaginator Objects</span>

The QueryNodePaginator class extends the QueryNode class and adds pagination-related functionality.
It keeps track of pagination state, appends pagination fields to the existing fields,
provides methods to check for a next page and update the pagination state,
and includes a method to reset the pagination state.

#### NOTE: We only implemented single level pagination, as multi-level pagination behavior is not well-defined in different scenarios. For example, you want to query all the pull requests a user made to all his/her repositories. You may develop a query that retrieves all repositories of a user as the first level pagination and all pull requests to each repository as the second level pagination. However, each repository not necessarily has the same number of pull requests. We leave this to the user to decide how they want to handle their multi-level pagination.

`class QueryNodePaginator(name, fields, args)`

- `name` is the name of the QueryNode.
- `fields` is a List of fields in the QueryNode.
- `args` is a Map of arguments in the QueryNode.

Instance methods:

`update_paginator(has_next_page, end_cursor)`

- update_paginator updates the paginator arguments with the provided has_next_page and end_cursor values. It adds the end cursor to the arguments using the key "after", enclosed in double quotes.

`has_next()`

- The has_next method checks if there is a next page by returning the value of has_next_page.

`reset_paginator()`

- The reset_paginator method resets the QueryPaginator by removing the "after" key from the arguments and setting has_next_page to None.

`__eq__(other)`

- \_\_eq\_\_ method overrides the equality comparison for QueryNodePaginator objects. It compares the object against another object of the same class, returning True if they are equal based on the parent class's equality comparison (super().**eq**(other)).

<span style="font-size: larger;">PaginatedQuery Objects</span>

`class PaginatedQuery(name, fields, args)`

- `name` is the name of the QueryNode
- `fields` is a List of fields in the QueryNode
- `args` is a Map of arguments in the QueryNode.
- The \_\_init\_\_ method initializes a PaginatedQuery object with the provided name, fields, and arguments. It calls the parent class's **init** method and then extracts the path to the pageInfo node using the extract_path_to_pageinfo_node static method.

`extract_path_to_pageinfo_node(paginated_query)`

- The extract_path_to_pageinfo_node static method is used to extract the path to the QueryNodePaginator node within the query. It takes a PaginatedQuery object as input and traverses the query fields to find the QueryNodePaginator. It returns a tuple containing the path to the QueryNodePaginator node and the QueryNodePaginator node. If the QueryNodePaginator node is not found, it raises an InvalidQueryException.

### client —

Source code: [github_graphql/client.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/client.py)

This class represents the main GitHub GraphQL client.

`class Client(protocol, host, is_enterprise, authenticator)`
_`protocol`: Protocol used for server communication.
_`host`: Host server domain or IP.
_`is_enterprise`: Boolean to check if the host is running on GitHub Enterprise.
_`authenticator`: The authentication handler for the client.

Private methods:

`_base_path(self)`:

- Returns the base path for a GraphQL request based on whether the client is connected to GitHub Enterprise.

`_generate_headers(self, **kwargs)`:

- Generates headers for an HTTP request, including authentication headers and other additional headers passed as keyword arguments.

`_retry_request(self, retry_attempts, timeout_seconds, query, substitutions)`:

- Wrapper method to retry requests. Takes in the number of attempts, timeout duration, the query, and the substitutions for the query.

`_execute(self, query, substitutions)`:

- Executes a GraphQL query after performing the required substitutions. Handles possible request errors and rate limiting.

`_execution_generator(self, query, substitutions)`:

- Executes a PaginatedQuery by repeatedly querying until all pages have been fetched. Yields each response.

Instance methods:

`execute(self, query, substitutions):`

- Executes a query, which can be a simple Query or a PaginatedQuery. Utilizes the \_execute method or the \_execution_generator method based on the type of query.

### user_login — Query for user basic login info

Source code: [queries/login.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/profile/user_login.py)

The `UserLoginViewer` class represents a GraphQL query that retrieves the login information of the currently authenticated user.
The query is defined using the Query class, and the viewer field is requested with the login field nested inside it.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query {
  viewer {
    login
  }
}
```

</td>
<td>

```python
class UserLoginViewer(Query):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "viewer",
                    fields=["login"]
                )
            ]
        )
```

</td>
</tr>
</table>

The `UserLogin` class represents a GraphQL query that retrieves detailed information about a user.
The query accepts a variable called $user of type String!, which represents the user's login. The user field is requested with the login argument set to the value of the $user variable. Inside the user field, additional fields like login, name, email, and createdAt are requested.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($user: String!){
    user(login: $user){
        login
        name
        id
        email
        createdAt
    }
}
```

</td>
<td>

```python
class UserLogin(Query):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={
                        "login": "$user"
                    },
                    fields=[
                        "login",
                        "name",
                        "id",
                        "email",
                        "createdAt"
                    ]
                )
            ]
        )
```

</td>
</tr>
</table>

### user_profile_stats — Query for user detailed profile info

Source code: [queries/login.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/profile/user_profile_stats.py)

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($user: String!){
    user(login: $user){
        login
        name
        id
        email
        createdAt
    }
}
```

</td>
<td>

```python
class UserProfileStats(Query):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        "name",
                        "email",
                        "createdAt",
                        "bio",
                        "company",
                        "isBountyHunter",
                        "isCampusExpert",
                        "isDeveloperProgramMember",
                        "isEmployee",
                        "isGitHubStar",
                        "isHireable",
                        "isSiteAdmin",
                        QueryNode("watching", fields=["totalCount"]),
                        QueryNode("starredRepositories", fields=["totalCount"]),
                        QueryNode("following", fields=["totalCount"]),
                        QueryNode("followers", fields=["totalCount"]),
                        QueryNode("gists", fields=["totalCount"]),
                        QueryNode("issues", fields=["totalCount"]),
                        QueryNode("projects", fields=["totalCount"]),
                        QueryNode("pullRequests", fields=["totalCount"]),
                        QueryNode("repositories", fields=["totalCount"]),
                        QueryNode("repositoryDiscussions", fields=["totalCount"]),
                        QueryNode("gistComments", fields=["totalCount"]),
                        QueryNode("issueComments", fields=["totalCount"]),
                        QueryNode("commitComments", fields=["totalCount"]),
                        QueryNode("repositoryDiscussionComments", fields=["totalCount"]),
                    ]
                )
            ]
        )
```

</td>
</tr>
</table>

### metrics — Query for user's total contribution metrics

Source code: [queries/metrics.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/metrics.py)

`UserMetrics` class represents a GraphQL query that retrieves various metrics and information about a user.
It is designed to fetch information such as the user's login, name, email, creation date, bio, company, and several other metrics related to their GitHub activity.
The root field in the query is "user", indicating that information about a specific user will be retrieved. The "user" field accepts an argument called "login", which represents the user's login.
Inside the "user" field, various other fields are requested, including "login", "name", "email", "createdAt", "bio", "company", and several other metrics related to the user's GitHub activity.
Some fields, such as "watching", "starredRepositories", "following", and "followers", have additional nested fields, specifically the "totalCount" field.
These nested fields allow you to retrieve the total count of certain metrics, such as the number of repositories a user is watching or the number of followers they have.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($user: String!) {
    user(login: $user) {
        login
        name
        email
        createdAt
        bio
        company
        isBountyHunter
        isCampusExpert
        isDeveloperProgramMember
        isEmployee
        isGitHubStar
        isHireable
        isSiteAdmin
        watching {
            totalCount
        }
        starredRepositories {
            totalCount
        }
        following {
            totalCount
        }
        followers {
            totalCount
        }
        gists {
            totalCount
        }
        gistComments {
            totalCount
        }
        issueComments {
            totalCount
        }
        issues {
            totalCount
        }
        projects {
            totalCount
        }
        pullRequests {
            totalCount
        }
        repositories {
            totalCount
        }
        repositoryDiscussionComments {
            totalCount
        }
        repositoryDiscussions {
            totalCount
        }
    }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    "login",
                    "name",
                    "email",
                    "createdAt",
                    "bio",
                    "company",
                    "isBountyHunter",
                    "isCampusExpert",
                    "isDeveloperProgramMember",
                    "isEmployee",
                    "isGitHubStar",
                    "isHireable",
                    "isSiteAdmin",
                    QueryNode("watching", fields=["totalCount"]),
                    QueryNode("starredRepositories", fields=["totalCount"]),
                    QueryNode("following", fields=["totalCount"]),
                    QueryNode("followers", fields=["totalCount"]),
                    QueryNode("gists", fields=["totalCount"]),
                    QueryNode("gistComments", fields=["totalCount"]),
                    QueryNode("issueComments", fields=["totalCount"]),
                    QueryNode("issues", fields=["totalCount"]),
                    QueryNode("projects", fields=["totalCount"]),
                    QueryNode("pullRequests", fields=["totalCount"]),
                    QueryNode("repositories", fields=["totalCount"]),
                    QueryNode("repositoryDiscussionComments", fields=["totalCount"]),
                    QueryNode("repositoryDiscussions", fields=["totalCount"]),
                ]
            )
        ]
    )
```

</td>
</tr>
</table>

### commits — Query for user's contribution metrics within a specified time range

Source code: [queries/commits.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/commits.py)

UserCommits represents a GraphQL query for retrieving commit-related contributions of a user within a specified time range.
Inside the "user" field, there is a nested field called "contributionsCollection". This field represents the collection of contributions made by the user.
The "contributionsCollection" field accepts two additional arguments, "from" and "to", with values of "$start" and "$end" respectively.
These variables represent the start and end dates of the time range for which the contributions are requested.
Inside the "contributionsCollection" field, several other fields are requested,
such as "startedAt", "endedAt", "hasActivityInThePast", "hasAnyContributions", "hasAnyRestrictedContributions", "restrictedContributionsCount", and various other commit-related metrics.
By including these fields in the query, you can retrieve information about the user's commit contributions, issue contributions, pull request contributions, and other related metrics within the specified time range.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($user: String!, $start: DateTime!, $end: DateTime!) {
    user(login: $user){
        contributionsCollection(from: $start,to: $end){
            startedAt
            endedAt
            hasActivityInThePast
            hasAnyContributions
            hasAnyRestrictedContributions
            restrictedContributionsCount
            totalCommitContributions
            totalIssueContributions
            totalPullRequestContributions
            totalPullRequestReviewContributions
            totalRepositoriesWithContributedCommits
            totalRepositoriesWithContributedIssues
            totalRepositoriesWithContributedPullRequestReviews
            totalRepositoriesWithContributedPullRequests
            totalRepositoryContributions
        }
    }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    QueryNode(
                        "contributionsCollection",
                        args={"from": "$start", "to": "$end"},
                        fields=[
                            "startedAt",
                            "endedAt",
                            "hasActivityInThePast",
                            "hasAnyContributions",
                            "hasAnyRestrictedContributions",
                            "restrictedContributionsCount",
                            "totalCommitContributions",
                            "totalIssueContributions",
                            "totalPullRequestContributions",
                            "totalPullRequestReviewContributions",
                            "totalRepositoriesWithContributedCommits",
                            "totalRepositoriesWithContributedIssues",
                            "totalRepositoriesWithContributedPullRequestReviews",
                            "totalRepositoriesWithContributedPullRequests",
                            "totalRepositoryContributions",
                        ]
                    ),
                ]
            )
        ]
    )
```

</td>
</tr>
</table>

### comments — Query for retrieving comments made by a user

Source code: [queries/comments.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/comments.py)

UserComments represents a GraphQL query for retrieving comments made by a user. The query structure includes a "user" field with the user's login as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator". This field represents the pagination of comments made by the user.
The "QueryNodePaginator" field accepts two additional arguments: "$comment_type" and "$pg_size". These arguments control the type of comments to retrieve and the pagination size, respectively. The value of "$comment_type" determines the type of comments to fetch, and the value of "$pg_size" sets the number of comments to retrieve per page.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "totalCount" to get the total count of comments, "nodes" to retrieve the comment nodes with their body and creation timestamps, and "pageInfo" to fetch pagination information such as the end cursor and whether there are more pages available.

#### NOTE: comment_type can be commitComments, gistComments, issueComments, and repositoryDiscussionComments.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!){
    user(login: $user){
        login
        issueComments(first: $pg_size){
            totalCount
            pageInfo{
                hasNextPage
                endCursor
            }
            nodes{
                body
                createdAt
            }
        }
    }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    "login",
                    QueryNodePaginator(
                        "$comment_type",
                        args={"first": "$pg_size"},
                        fields=[
                            "totalCount",
                            QueryNode(
                                "nodes",
                                fields=["body", "createdAt"]
                            ),
                            QueryNode(
                                "pageInfo",
                                fields=["endCursor", "hasNextPage"]
                            )
                        ]
                    )
                ]
            )
        ]
    )
```

</td>
</tr>
</table>

### contributions — Query for retrieving contributions made by a user

Source code: [queries/contributions.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/contributions.py)

UserContributions represents a GraphQL query for retrieving contributions made by a user. The query structure includes a "user" field with the user's login as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator".
This field represents the pagination of contributions made by the user. The "QueryNodePaginator" field accepts two additional arguments: "$contribution_type" and "$pg_size". These arguments control the type of contributions to retrieve and the pagination size, respectively.
The value of "$contribution_type" determines the type of contributions to fetch, such as "issue", "pullRequest", or any other valid contribution type. The value of "$pg_size" sets the number of contributions to retrieve per page.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "totalCount" to get the total count of contributions, "nodes" to retrieve the contribution nodes with their creation timestamps, and "pageInfo" to fetch pagination information such as the end cursor and whether there are more pages available.

#### NOTE: contribution_type can be any valid contribution type such as "issues" or "pullRequests"

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!){
    user(login: $user){
        login
        issues(first:$pg_size){
            totalCount
            pageInfo{
                hasNextPage
                endCursor
            }
            nodes{
                createdAt
            }
        }
    }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    "login",
                    QueryNodePaginator(
                        "$contribution_type",
                        args={"first": "$pg_size"},
                        fields=[
                            "totalCount",
                            QueryNode(
                                "nodes",
                                fields=["createdAt"]
                            ),
                            QueryNode(
                                "pageInfo",
                                fields=["endCursor", "hasNextPage"]
                            )
                        ]
                    )
                ]
            )
        ]
    )
```

</td>
</tr>
</table>

### repositories — Query for retrieving repositories owned or contributed to by a user

Source code: [queries/repositories.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/repositories.py)

UserRepositories represents a GraphQL query for retrieving repositories owned or contributed to by a user. The query structure includes a "user" field with the user's login as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator".
This field represents the pagination of repositories. The "QueryNodePaginator" field accepts several arguments that allow for filtering and ordering the repositories. These arguments include "$pg_size" to set the pagination size, "$is_fork" to filter by whether the repository is a fork, "$ownership" to filter by owner affiliations, and "$order_by" to specify the field and direction for ordering the repositories.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "nodes" to retrieve information about the repositories. Each repository node includes various details such as the repository name, whether it is empty, creation and update timestamps, fork count, stargazer count, total watcher count, primary programming language, and information about the languages used in the repository.
The "languages" field provides information about the languages used in the repository. It accepts additional arguments for filtering and ordering the languages. The requested fields within the "languages" field include "totalSize" to get the total size of the languages used, "totalCount" to get the count of distinct languages, and "edges" to retrieve detailed information about each language, including its size and name.

#### NOTE: isFork can be "True" or "False", ownerAffiliation can be "OWNER" or "COLLABORATOR"

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!, $isFork: Boolean!, $ownerAffiliations: [RepositoryAffiliation!]!) {
    user(login: $user) {
        repositories(first: $pg_size, isFork: $isFork, ownerAffiliations: $ownerAffiliations, orderBy: { field: CREATED_AT, direction: ASC }) {
            totalCount
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                name
                isEmpty
                createdAt
                updatedAt
                forkCount
                stargazerCount
                watchers {
                    totalCount
                }
                primaryLanguage {
                    name
                }
                languages(first: 100) {
                    totalSize
                    totalCount
                    edges {
                        size
                        node {
                            name
                        }
                    }
                }
            }
        }
    }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    QueryNodePaginator(
                        "repositories",
                        args={"first": "$pg_size",
                              "isFork": "$is_fork",
                              "ownerAffiliations": "$ownership",
                              "orderBy": "$order_by"},
                        fields=[
                            QueryNode(
                                "nodes",
                                fields=[
                                    "name",
                                    "isEmpty",
                                    "createdAt",
                                    "updatedAt",
                                    "forkCount",
                                    "stargazerCount",
                                    QueryNode("watchers", fields=["totalCount"]),
                                    QueryNode("primaryLanguage", fields=["name"]),
                                    QueryNode(
                                        "languages",
                                        args={"first": 100,
                                              "orderBy": {"field": "SIZE",
                                                          "direction": "DESC"}},
                                        fields=[
                                            "totalSize",
                                            "totalCount",
                                            QueryNode(
                                                "edges",
                                                fields=[
                                                    "size",
                                                    QueryNode("node", fields=["name"])
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            QueryNode(
                                "pageInfo",
                                fields=["endCursor", "hasNextPage"]
                            )
                        ]
                    ),
                ]
            )
        ]
    )
```

</td>
</tr>
</table>

### repository_contributors — Query for retrieving contributors of a repository

Source code: [queries/repository_contributors.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/repository_contributors.py)

This GraphQL query aims to retrieve the default branch reference of a specified repository.
Specifically, it extracts the login names of authors from the commit history of the default branch.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef {
      target {
        ... on Commit {
          history{
            nodes {
              author {
                user {
                  login
                }
              }
            }
          }
        }
      }
    }
  }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "repository",
                args={"owner": "$owner",
                      "name": "$repo_name"},
                fields=[
                    QueryNode(
                        "defaultBranchRef",
                        fields=[
                            QueryNode(
                                "target",
                                fields=[
                                    QueryNode(
                                        "... on Commit",
                                        fields=[
                                            QueryNode(
                                                "history",
                                                fields=[
                                                    QueryNode(
                                                        "nodes",
                                                        fields=[
                                                            QueryNode(
                                                                "author",
                                                                fields=[
                                                                    QueryNode(
                                                                        "user",
                                                                        fields=[
                                                                            "login"
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
```

</td>
</tr>
</table>

### repository_contributors_contribution — Query for retrieving contributions of a contributor made to a repository

Source code: [queries/repository_contributors_contribution.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/repository_contributors_contribution.py)

This GraphQL query is designed to retrieve the commit history of a specified author ($id) 
in the default branch of a specified repository ($owner and $name).
It returns key metrics like the total count of commits, the date each commit was authored, the number of changed files,
additions, and deletions for each commit, along with the author's login name.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($owner: String!, $name: String!, $id: ID!, $pg_size: Int!){
  repository(owner: $owner, name: $name) {
    defaultBranchRef {
      target {
        ... on Commit {
          history(author: { id: $id }, first: $pg_size) {
            totalCount
            nodes {
              authoredDate
              changedFilesIfAvailable
              additions
              deletions
              author {
                user {
                  login
                }
              }
            }
            pageInfo {
              endCursor
              hasNextPage
            }
          }
        }
      }
    }
  }
}
```

</td>
<td>

```python
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "repository",
                    args={"owner": "$owner",
                          "name": "$repo_name"},
                    fields=[
                        QueryNode(
                            "defaultBranchRef",
                            fields=[
                                QueryNode(
                                    "target",
                                    fields=[
                                        QueryNode(
                                            "... on Commit",
                                            fields=[
                                                QueryNode(
                                                    "history",
                                                    args={"author": "$id"},
                                                    fields=[
                                                        "totalCount",
                                                        QueryNode(
                                                            "nodes",
                                                            fields=[
                                                                "authoredDate",
                                                                "changedFilesIfAvailable",
                                                                "additions",
                                                                "deletions",
                                                                QueryNode(
                                                                    "author",
                                                                    fields=[
                                                                        QueryNode(
                                                                            "user",
                                                                            fields=[
                                                                                "login"
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
```

</td>
</tr>
</table>

### repositories — Query for retrieving commits af a contributor made to a repository

Source code: [queries/repository_commits.py]()

This GraphQL query is structured to retrieve commits from the default branch of a specified repository. For each commit, it fetches the authored date, the number of changed files (if available), the number of additions and deletions, the commit message, and details about the commit's author.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($owner: String!, $repo_name: String!, $pg_size: Int!) {
  repository(owner: $owner, name: $repo_name) {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: $pg_size) {
            totalCount
            nodes {
              authoredDate
              changedFilesIfAvailable
              additions
              deletions
              message
              parents (first: 2) {
                totalCount
              }
              author {
                name
                email
                user {
                  login
                }
              }
            }
            pageInfo {
              endCursor
              hasNextPage
            }
          }
        }
      }
    }
  }
}
```

</td>
<td>

```python
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "repository",
                    args={"owner": "$owner",
                          "name": "$repo_name"},
                    fields=[
                        QueryNode(
                            "defaultBranchRef",
                            fields=[
                                QueryNode(
                                    "target",
                                    fields=[
                                        QueryNode(
                                            "... on Commit",
                                            fields=[
                                                QueryNodePaginator(
                                                    "history",
                                                    args={"first": "$pg_size"},
                                                    fields=[
                                                        'totalCount',
                                                        QueryNode(
                                                            "nodes",
                                                            fields=[
                                                                "authoredDate",
                                                                "changedFilesIfAvailable",
                                                                "additions",
                                                                "deletions",
                                                                "message",
                                                                QueryNode(
                                                                    "parents (first: 2)",
                                                                    fields=[
                                                                        "totalCount"
                                                                    ]
                                                                ),
                                                                QueryNode(
                                                                    "author",
                                                                    fields=[
                                                                        'name',
                                                                        'email',
                                                                        QueryNode(
                                                                            "user",
                                                                            fields=[
                                                                                "login"
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        QueryNode(
                                                            "pageInfo",
                                                            fields=["endCursor", "hasNextPage"]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
```

</td>
</tr>
</table>

### ratelimit —

Source code: [queries/rate_limit.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/rate_limit.py)

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($dryrun: Boolean!){
  rateLimit (dryRun: $dryrun){
    cost
    limit
    remaining
    resetAt
    used
  }
}

```

</td>
<td>

```python

```

</td>
</tr>
</table>
