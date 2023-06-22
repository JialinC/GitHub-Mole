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


## authentication  — Basic authenticator class
Source code: [github_graphql/authentication.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/github_graphql/authentication.py)

This model provides the basic authentication mechanism. User needs to provide a valid GitHub PAT with correct scope to run queries. 
A PersonalAccessTokenAuthenticator object will be created with the PAT that user provided. get_authorization_header method will return an
 authentication header that will be used when send request to GitHub GraphQL server.

<span style="font-size: larger;">Authenticator Objects</span>

Parent class of PersonalAccessTokenAuthenticator. Serve as base class of any authenticators.

<span style="font-size: larger;">PersonalAccessTokenAuthenticator Objects</span>

Handles personal access token authentication method for GitHub clients.

class PersonalAccessTokenAuthenticator(token)
* The token argument is required. This is the user's GitHub personal access token with the necessary scope to execute the queries that the user required.

Instance methods:

get_authorization_header()
* Returns the authentication header as a dictionary {"Authorization": "your_access_token"}.