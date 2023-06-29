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

### query  — Classes for building GraphQL queries
Source code: [github_graphql/query.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/query.py)

This module provides a framework for building GraphQL queries using Python classes. The code defines four classes: QueryNode, QueryNodePaginator, Query, and PaginatedQuery.
QueryNode represents a basic building block of a GraphQL query. 
QueryNodePaginator is a specialized QueryNode for paginated requests. 
Query represents a terminal query node that can be executed. 
PaginatedQuery represents a terminal query node designed for paginated requests.
* You can find more information about GitHub GraphQL API here: [GitHub GraphQL API documentation](https://docs.github.com/en/graphql)
* You can use GitHub GraphQL Explorer to try out queries: [GitHub GraphQL API Explorer](https://docs.github.com/en/graphql/overview/explorer)

<span style="font-size: larger;">QueryNode Objects</span>

The QueryNode class provides a framework for constructing GraphQL queries using Python classes. 
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

<span style="font-size: larger;">Query Objects</span>

The Query class is a subclass of QueryNode and represents a terminal QueryNode that can be executed. 
It provides a substitute method to substitute values in the query using keyword arguments.

Instance methods:

`substitute(**kwargs)`
* This method substitutes the placeholders in the query string with specific values provided as keyword arguments.

<span style="font-size: larger;">QueryNodePaginator Objects</span>

The QueryNodePaginator class extends the QueryNode class and adds pagination-related functionality. 
It keeps track of pagination state, appends pagination fields to the existing fields, 
provides methods to check for a next page and update the pagination state, 
and includes a method to reset the pagination state.

#### NOTE: We only implemented single level pagination, as multi-level pagination behavior is not well-defined in different scenarios. For example, you want to query all the pull requests a user made to all his/her repositories. You may develop a query that retrieves all repositories of a user as the first level pagination and all pull requests to each repository as the second level pagination. However, each repository not necessarily has the same number of pull requests. We leave this to the user to decide how they want to handle their multi-level pagination.

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



<span style="font-size: larger;">PaginatedQuery Objects</span>

### client  — 
Source code: [github_graphql/client.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/client.py)

This module contains




### login  — Query for user basic login info
Source code: [queries/login.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/login.py)

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
query = Query(
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
        email
        createdAt
    }
}
```

</td>
<td>

```python
query = Query(
        fields=[
            QueryNode(
                "user",
                args={
                    "login": "$user"
                },
                fields=[
                    "login", 
                    "name", 
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

### metrics  — Query for user's total contribution metrics
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
query = Query(
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

### commits  — Query for user's contribution metrics within a specified time range
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
    user(login: "$user"){
        contributionsCollection(from:"$start",to:"$end"){
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
query = Query(
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

### comments  — 
Source code: [queries/comments.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/comments.py)

### contributions  — 
Source code: [queries/contributions.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/contributions.py)

### repositories  — 
Source code: [queries/repositories.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/repositories.py)

### repositories_graph —
Source code: [queries/repositories_graph.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/repository_graph.py)

### repositories  — 
Source code: [miners/repositories.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/miners/repositories.py)
