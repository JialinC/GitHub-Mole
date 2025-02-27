📖 **Documentation Menu**  
🔹 [🏠 Home](index.md)  
🔹 [📥 Installation](installation.md)  
🔹 [🛠 Usage Guide](usage.md)  
🔹 [⚙️ API Documentation](api.md)
🔹 [📓 Database Schema](schema.md)

# ⚙️ API Documentation

These APIs should only be called by the frontend code. 

Most of the APIs require a JWT token.

## 📘 Authentication API Documentation

### 📌 Authentication

All endpoints do not require authentication using JWT tokens.

### 1️⃣ Initiate OAuth Authorization

Initiates the OAuth login process by redirecting the user to GitHub's authorization page.

🔹 Request

Method: GET

URL: /oauth/authorize

🔹 Response

|Status Code   |Description   |
|:-------------|:-------------|
|302 Found     |Redirects to GitHub's OAuth authorization page.|


### 2️⃣ OAuth Callback Handling

Handles the response from GitHub after the user authorizes the application. It exchanges the authorization code for an access token, retrieves user data, and generates JWT tokens.

🔹 Request

Method: GET

URL: /oauth/callback

🔹 Response

|Status Code   |Description   |
|:-------------|:-------------|
|302 Found     |Redirects the user to the frontend with access and refresh tokens.|
|400 Bad Request|Authorization failed or invalid response from GitHub.|


### 3️⃣ User Logout

Clears session data and logs the user out.

🔹 Request

Method: GET

URL: /oauth/logout

🔹 Response

|Status Code   |Description|
|:-------------|:-------------|
|302 Found     |Redirects to the index page.|


## 📘 Helper API Documentation

This API provides various helper functions, including SSO configuration checks, PAT validation, user info retrieval, token refresh, and duplicate checks.

### 📌 Authentication

All endpoints require authentication using JWT tokens.

### 1️⃣ Check Single Sign-On (SSO) Configuration

Returns whether GitHub SSO (Single Sign-On) is configured.

🔹 Request

Method: GET

URL: /helper/sso

Headers: No authentication required.

🔹 Response

|Status Code   |Description|
|:-------------|:-------------|
|200 OK	       |Returns whether SSO is configured.|


### 2️⃣ Validate Personal Access Token (PAT)

Validates a GitHub Personal Access Token (PAT) and retrieves the authenticated user's details.

🔹 Request

Method: POST

URL: /helper/validate-pat

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description|
|:------------|:------------|:------------|:------------|
|pat	      |string	    |✅ Yes	     |The Personal Access Token for authentication.|
|accountType  |string	    |✅ Yes	     |Type of GitHub account (e.g., personal, enterprise).|
|apiUrl	      |string	    |✅ Yes	     |The base API URL for the GitHub instance.|

🔹 Response

|Status Code  |Description  |
|:------------|:------------|
|200 OK	      |PAT is valid, returns JWT tokens.|
|400 Bad Request|Invalid PAT or unable to authenticate.|
|500 Internal Server Error|	Unexpected server error.|


### 3️⃣ Retrieve User Information

Fetches the authenticated user's GitHub profile information.

🔹 Request

Method: GET

URL: /helper/user-info

🔹 Response

|Status Code  |Description  |
|:------------|:------------|
|200 OK	       |Returns user details.|
|401 Unauthorized|	Invalid or missing token.|
|404 Not Found   |	User not found.|
|500 Internal Server Error|	Unexpected error.|

### 4️⃣ Refresh Access Token

Generates a new access token using a valid refresh token.

🔹 Request

Method: POST

URL: /helper/refresh

🔹 Response

|Status Code  |Description|
|:------------|:------------|
|200 OK	      |Returns a new access token.|
|401 Unauthorized|	Invalid or expired refresh token.|


### 5️⃣ Check for Duplicate Entries

Checks if a dataset with the given name and type already exists for the authenticated user.

🔹 Request

Method: GET

URL: /helper/check-duplicate?name=dataset_name&type=data_type

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description|
|:------------|:------------|:------------|:------------|
|name	      |string	    |✅ Yes	     |The name of the dataset.|
|type	      |string	    |✅ Yes	     |The type of the dataset.|

🔹 Response

|Status Code  |Description  |
|:------------|:------------|
|200 OK	      |Returns whether the dataset exists.|
|401 Unauthorized|	Invalid or missing token.|


## 📘 GitHub Query API Endpoints

These API endpoints interact with GitHub's GraphQL and REST APIs to retrieve user details, contributions, repositories, commits, and more.

### 📌 Authentication

All endpoints require authentication using JWT tokens.

### 1️⃣ Get API Rate Limits

This endpoint retrieves the rate limit information for the authenticated GitHub user. It provides details about API quota, cost per request, remaining quota, and reset time

🔹 Request

Method: GET

URL: /api/graphql/rate-limit

🔹 Response

|Status Code  |Description|
|:------------|:------------|
|200 OK	|Returns rate limit details.|
|401 Unauthorized|	Missing or invalid JWT token.|
|500 Internal Server Error|	Server error occurred.|


### 2️⃣ Get Current User Login

This API endpoint retrieves the GitHub login details of the currently authenticated user using their OAuth token.

🔹 Request

Method: GET

URL: /api/graphql/current-user-login

🔹 Response

|Status Code  |Description|
|:------------|:------------|
|200 OK	      |Returns current user's GitHub login.|
|401 Unauthorized|	Invalid or missing token.|

### 3️⃣ Get Specific User Login

This API endpoint retrieves the GitHub login details of a specific user by their username.

🔹 Request

Method: GET

URL: /api/graphql/user-login/{login}

🔹 Response

|Status Code  |Description|
|:------------|:------------|
|200 OK	      |Returns the specified user's GitHub login details.|
|401 Unauthorized|Missing or invalid JWT token.|
|404 Not Found |The requested GitHub user does not exist.|
|500 Internal Server Error|	Server error occurred.|


### 4️⃣ Get User Profile Statistics

This API endpoint retrieves detailed statistical information about a specific GitHub user's profile, including their contributions, repositories, followers, and other profile-related metrics.

🔹 Request

Method: GET

URL: /api/graphql/user-profile-stats/{login}

🔹 Response

|Status Code  |Description|
|:------------|:------------|
|200 OK	|Returns the specified user's GitHub profile statistics.|
|401 Unauthorized|	Missing or invalid JWT token.|
|404 Not Found|	The requested GitHub user does not exist.|
|500 Internal Server Error|	Server error occurred.|


### 5️⃣ Get User Contributions

This endpoint retrieves a GitHub user's contributions over a specified period, including commits, issues, pull requests, PR reviews, and repository contributions.

🔹 Request

Method: GET

URL: /api/graphql/user-contributions-collection/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|start	      |string (YYYY-MM-DD)|	❌ No |Start date for fetching contributions (default: user account creation date).|
|end	      |string (YYYY-MM-DD)|	❌ No |End date for fetching contributions (default: current date).|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns user contributions.|
|401 Unauthorized|	Missing or invalid JWT token.|
|404 Not Found|	The requested GitHub user does not exist.|
|500 Internal Server Error|	Server error occurred.|


### 6️⃣ Get User Contribution Years

This API endpoint retrieves the years in which a GitHub user has made contributions (e.g., commits, issues, pull requests). It provides an overview of the active contribution periods for a given user.

🔹 Request

Method: GET

URL: /api/graphql/user-contribution-years/{login}

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns a list of years when the user has contributed.|
|401 Unauthorized|	Missing or invalid JWT token.|
|404 Not Found|	The requested GitHub user does not exist.|
|500 Internal Server Error|	Server error occurred.|

### 7️⃣ Get GitHub User Contribution Calendar

This API endpoint retrieves the contribution calendar for a GitHub user, displaying their activity (e.g., commits, issues, PRs) over a specific period.

🔹 Request

Method: GET

URL: /api/graphql/user-contribution-calendar/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|start	      |string	    |❌ No	    |Start date for the calendar (format: YYYY-MM-DD).|
|end	      |string	    |❌ No       |End date for the calendar (format: YYYY-MM-DD).|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the user's contribution calendar.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|Server error occurred.|

### 8️⃣ Get User Repositories (Type A)

This API endpoint retrieves non-forked repositories owned by a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-repositories-a/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns the user's owned repositories.|
|401 Unauthorized|	Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 9️⃣ Get User Repositories (Type B)

This API endpoint retrieves forked repositories owned by a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-repositories-b/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the user's owned repositories.|
|401 Unauthorized|	Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|


### 1️⃣0️⃣ Get User Repositories (Type C)

This API endpoint retrieves non-forked repositories where a GitHub user is a collaborator.

🔹 Request

Method: GET

URL: /api/graphql/user-repositories-a/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns the user's repositories where they are a collaborator.|
|401 Unauthorized|	Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 1️⃣1️⃣ Get User Repositories (Type D)

This API endpoint retrieves forked repositories where a GitHub user is a collaborator.

🔹 Request

Method: GET

URL: /api/graphql/user-repositories-a/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns the user's repositories where they are a collaborator.|
|401 Unauthorized|	Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|


### 1️⃣2️⃣ Get User Commit Comments

This API endpoint retrieves a paginated list of commit comments made by a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-commit-comments/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns the user's commit comments.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 1️⃣3️⃣ Get User Gist Comments

This API endpoint retrieves a paginated list of gist comments made by a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-gist-comments/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns the user's gist comments.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 1️⃣4️⃣ Get User Issue Comments

This API endpoint retrieves paginated issue comments made by a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-issue-comments/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns the user's issue comments.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 1️⃣5️⃣ Get User Repository Discussion Comments

This API endpoint retrieves paginated discussion comments made by a GitHub user in repository discussions.

🔹 Request

Method: GET

URL: /api/graphql/user-repository-discussion-comments/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	|Returns the user's repository discussion comments.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|


### 1️⃣6️⃣ Get User Gists

This API endpoint retrieves paginated gists created by a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-gists/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the user's gists.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 1️⃣7️⃣ Get User Issues

This API endpoint retrieves paginated issues associated with a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-issues/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the user's issues.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 1️⃣8️⃣ Get User Pull Requests

This API endpoint retrieves paginated pull requests associated with a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-pull-requests/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the user's pull requests.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|


### 1️⃣9️⃣ Get User Repository Discussions

This API endpoint retrieves paginated discussions within repositories owned by a GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user-repository-discussions/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the user's repository discussions.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 2️⃣0️⃣ Get Repository Branches

This API endpoint retrieves paginated branches for a specified GitHub repository.

🔹 Request

Method: GET

URL: /api/graphql/repository_branches/{owner}/{repo}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the repository branches.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 2️⃣1️⃣ Get Repository Default Branch

This API endpoint retrieves the default branch for a given GitHub repository.

🔹 Request

Method: GET

URL: /api/graphql/repository_default_branch/{owner}/{repo}

🔹 Query Parameters

|Parameter	|Type	|Required	|Description|
|:------------|:------------|:------------|:------------|
|owner	      |string	    |✅ Yes	     |GitHub username or organization name.|
|repo	      |string	    |✅ Yes	     |The name of the repository.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the default branch of the repository.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 2️⃣2️⃣ Get Repository Contributors

This API endpoint retrieves the contributors of a given GitHub repository's default branch.

🔹 Request

Method: GET

URL: /api/graphql/repository_contributors/{owner}/{repo}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|owner	      |string	    |✅ Yes	    |GitHub username or organization name.|
|repo	      |string	    |✅ Yes	    |The name of the repository.|
|end_cursor	  |string	    |❌ No	    |Cursor for pagination, to fetch the next set of results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the contributors of the repository.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 2️⃣3️⃣ Get Repository Branch Commits

This API endpoint retrieves the commit history for a specific branch of a GitHub repository.

🔹 Request

Method: GET

URL: /api/graphql/repository_branch_commits/{owner}/{repo}/{use_default}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|owner	      |string	    |✅ Yes	     |GitHub username or organization name.|
|repo	      |string	    |✅ Yes	     |The name of the repository.|
|use_default  |bool	        |✅ Yes	     |Whether to fetch commits from the default branch.|
|branch	      |string	    |❌ No	     |The branch name (required if use_default is False).|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the commit history of the branch.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 2️⃣4️⃣ Get User Repository Names

This API endpoint retrieves the names of all repositories associated with a specific GitHub user.

🔹 Request

Method: GET

URL: /api/graphql/user_repository_names/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|login	      |string	    |✅ Yes	     |GitHub username of the user.|
|end_cursor	  |string	    |❌ No	     |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the list of repository names for the user.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 2️⃣5️⃣ Get Contributor Contributions to a Repository

This API endpoint retrieves commit contributions made by a specific GitHub user to a repository.

🔹 Request

Method: GET

URL: /api/graphql/repository_contributor_contributions/{owner}/{repo}/{login}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|owner	      |string	    |✅ Yes	    |GitHub username of the repository owner.|
|repo	      |string	    |✅ Yes	    |Repository name.|
|login	      |string	    |✅ Yes	    |GitHub username of the contributor.|
|branch	      |string	    |❌ No	    |Branch name to filter commits (default: default branch).|
|end_cursor	  |string	    |❌ No	    |Cursor for paginated results.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns the list of commit contributions for the user.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 2️⃣6️⃣ Get GitHub Commit Details

This API endpoint retrieves commit details from GitHub, including author information, message, stats, and language breakdown. It also implements rate-limiting handling and retry logic.

🔹 Request

Method: GET

URL: /api/rest/commits/{owner}/{repo}/{sha}

🔹 URL Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|owner	      |string	    |✅ Yes	    |GitHub username of the repository owner.|
|repo	      |string	    |✅ Yes	    |Repository name.|
|sha	      |string	    |✅ Yes	    |SHA of the commit.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns commit details.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested GitHub user does not exist.|
|500 Internal Server Error	|A server error occurred.|


## 📘 SDE Team Formation API Endpoints

This API endpoint forms teams based on provided user attributes using constrained K-Means clustering.

### 📌 Authentication

All endpoints require authentication using JWT tokens.

### 1️⃣ Forms Teams

Forms teams based on provided attributes using clustering.

🔹 Request

Method: POST

URL: /api/team/form-team

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|columns	  |dict	        |✅ Yes	     |Dictionary where keys represent attributes, and values are lists of corresponding user attributes.|
|teamSize	  |int	        |✅ Yes	     |The number of teams to form.|
|allowExceed  |bool	        |✅ Yes	     |Whether to allow some teams to have one extra member.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Successfully formed teams.|
|400 Bad      |Request	Invalid input data.|
|500 Internal Server Error	|Error occurred during team formation.|

## 📘 Database Interaction API Endpoints

This API allows users to store, retrieve, and manage their GitHub-related datasets, including repositories, commits, issues, PRs, and discussions.

### 📌 Authentication

All endpoints require authentication using JWT tokens.

### 1️⃣ Check for Duplicate Dataset

This API endpoint checks if a dataset with the given name and type already exists for the authenticated user.

🔹 Request

Method: POST

URL: /api/db/check-duplicate

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|name	      |string	    |✅ Yes	    |The name of the dataset to check.|
|type	      |string	    |✅ Yes	    |Type of dataset (e.g., "Repositories", "Issues", "Pull Requests").|

🔹 Response

|Status |Code	Description|
|:------------|:------------|
|200 OK	|Returns whether the dataset exists.|
|401 Unauthorized	|Missing or invalid JWT token.|
|500 Internal Server Error	|A server error occurred.|


### 2️⃣ Save Dataset to Database

This API endpoint saves user-generated data into the database.

🔹 Request

Method: POST

URL: /api/db/save-data

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|name	      |string	    |✅ Yes	    |The name of the dataset.|
|type	      |string	    |✅ Yes	    |Type of dataset (e.g., "Repositories", "Issues", "Pull Requests").|
|tableHeader  |list	        |✅ Yes	    |Column headers for the dataset.|
|tableData	  |list	        |✅ Yes	    |Rows of data matching the table headers.|
|langs	      |list	        |❌ No	    |(For repositories) List of languages.|
|startTime	  |string	    |❌ No	    |(Optional) Start time for data filtering.|
|endTime	  |string	    |❌ No	    |(Optional) End time for data filtering.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Data successfully saved.|
|401 Unauthorized	|Missing or invalid JWT token.|
|500 Internal Server Error	|Failed to save data.|

### 3️⃣ Get User Queries

This API endpoint retrieves all queries made by the authenticated user.

🔹 Request

Method: GET

URL: /api/db/user-queries

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns a list of datasets created by the user.|
|401 Unauthorized	|Missing or invalid JWT token.|
|500 Internal Server Error	|A server error occurred.|

### 4️⃣ Delete a User Query

This API endpoint deletes a specific user query.

🔹 Request

Method: DELETE

URL: /api/db/user-queries/{query_id}

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|query_id	  |string	    |✅ Yes	     |GitHub username of the user.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Query successfully deleted.|
|401 Unauthorized	|Missing or invalid JWT token.|
|500 Internal Server Error	|Failed to delete query.|

### 5️⃣ Retrieve Contributions of a Query

This API endpoint retrieves user contributions based on the specified query ID.

🔹 Request

Method: GET

URL: /api/db/user-queries/{query_id}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|query_id	  |int	        |✅ Yes	|The ID of the user query to retrieve contributions for.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Returns contributions for the dataset.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested query does not exist.|
|500 Internal Server Error	|A server error occurred.|

### 6️⃣ Delete a Specific Contribution

This API endpoint deletes a specific contribution from a user query.

🔹 Request

Method: DELETE

URL: /api/db/user-contributions/{query_id}/{contribution_id}

🔹 Query Parameters

|Parameter	  |Type	        |Required	  |Description  |
|:------------|:------------|:------------|:------------|
|query_id	  |int	        |✅ Yes	     |The ID of the user query.|
|contribution_id	|int	|✅ Yes	     |The ID of the contribution to be deleted.|

🔹 Response

|Status Code  |	Description |
|:------------|:------------|
|200 OK	      |Contribution successfully deleted.|
|401 Unauthorized	|Missing or invalid JWT token.|
|404 Not Found	|The requested contribution does not exist.|
|500 Internal Server Error	|A server error occurred.|







