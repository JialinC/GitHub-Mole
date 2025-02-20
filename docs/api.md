📖 **Documentation Menu**  
🔹 [🏠 Home](index.md)  
🔹 [📥 Installation](installation.md)  
🔹 [🛠 Usage Guide](usage.md)  
🔹 [⚙️ API Documentation](api.md)  

# ⚙️ API Documentation
## Published Backend API
### 📘 Authentication API Documentation
1️⃣ Initiate OAuth Authorization

GET /oauth/authorize

Initiates the OAuth login process by redirecting the user to GitHub's authorization page.

🔹 Request

Method: GET

URL: /oauth/authorize

Headers: No authentication required.

🔹 Response

|Status Code   |Description   |
|:-------------|:-------------|
|302 Found     |Redirects to GitHub's OAuth authorization page.|


2️⃣ OAuth Callback Handling

GET /oauth/callback

Handles the response from GitHub after the user authorizes the application. It exchanges the authorization code for an access token, retrieves user data, and generates JWT tokens.

🔹 Request

Method: GET

URL: /oauth/callback

Headers: No authentication required.

🔹 Response

|Status Code   |Description   |
|:-------------|:-------------|
|302           |Found	Redirects the user to the frontend with access and refresh tokens.|
|400           |Bad Request	Authorization failed or invalid response from GitHub.|


3️⃣ User Logout

GET /oauth/logout

Clears session data and logs the user out.

🔹 Request

Method: GET

URL: /oauth/logout

Headers: No authentication required.

🔹 Response
|Status Code   |Description|
|:-------------|:-------------|
|302 Found     |Redirects to the index page.|


### 📘 Helper API Documentation
This API provides various helper functions, including SSO configuration checks, PAT validation, user info retrieval, token refresh, and duplicate checks.

1️⃣ Check Single Sign-On (SSO) Configuration

GET /helper/sso

Returns whether GitHub SSO (Single Sign-On) is configured.

🔹 Request

Method: GET

URL: /helper/sso

Headers: No authentication required.

🔹 Response

|Status Code   |Description|
|:-------------|:-------------|
|200 OK	       |Returns whether SSO is configured.|


2️⃣ Validate Personal Access Token (PAT)

POST /helper/validate-pat

Validates a GitHub Personal Access Token (PAT) and retrieves the authenticated user's details.

🔹 Request

Method: POST

URL: /helper/validate-pat

Headers: Content-Type: application/json

Body Parameters:

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


3️⃣ Retrieve User Information

GET /helper/user-info

Fetches the authenticated user's GitHub profile information.

🔹 Request

Method: GET

URL: /helper/user-info

Headers: Authorization: Bearer YOUR_ACCESS_TOKEN
(JWT Refresh Token required)

🔹 Response

|Status Code  |Description  |
|:------------|:------------|
|200 OK	       |Returns user details.|
|401 Unauthorized|	Invalid or missing token.|
|404 Not Found   |	User not found.|
|500 Internal Server Error|	Unexpected error.|

4️⃣ Refresh Access Token

POST /helper/refresh

Generates a new access token using a valid refresh token.

🔹 Request

Method: POST

URL: /helper/refresh

Headers: Authorization: Bearer YOUR_REFRESH_TOKEN

(JWT Refresh Token required)

🔹 Response

|Status Code  |Description|
|:------------|:------------|
|200 OK	      |Returns a new access token.|
|401 Unauthorized|	Invalid or expired refresh token.|


5️⃣ Check for Duplicate Entries

GET /helper/check-duplicate

Checks if a dataset with the given name and type already exists for the authenticated user.

🔹 Request

Method: GET

URL: /helper/check-duplicate?name=dataset_name&type=data_type

Headers: Authorization: Bearer YOUR_ACCESS_TOKEN
(JWT Token required)

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











