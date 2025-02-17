📖 **Documentation Menu**  
🔹 [🏠 Home](index.md)  
🔹 [📥 Installation](installation.md)  
🔹 [🛠 Usage Guide](usage.md)  
🔹 [⚙️ API Documentation](api.md)  

# ⚙️ API Documentation
## Published Backend API
### 📌 Authentication

1️⃣ Initiate OAuth Authorization
GET /oauth/authorize
Initiates the OAuth login process by redirecting the user to GitHub's authorization page.

🔹 Request

Method: GET

URL: /oauth/authorize

Headers: No authentication required.

🔹 Response

| Status Code | Description |
|-------------|-------------|
| 302 Found   | Redirects to GitHub's OAuth authorization page. |

🔹 Example Usage

curl -X GET "https://your-api.com/oauth/authorize"

Response:
The user is redirected to:
https://github.com/login/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI

2️⃣ OAuth Callback Handling
GET /oauth/callback
Handles the response from GitHub after the user authorizes the application. It exchanges the authorization code for an access token, retrieves user data, and generates JWT tokens.

🔹 Request

Method: GET

URL: /oauth/callback

Headers: No authentication required.

🔹 Response

|Status Code  |	Description |
|-------------|-------------|
|302 |Found	Redirects the user to the frontend with access and refresh tokens.|
|400 |Bad Request	Authorization failed or invalid response from GitHub.|

🔹 Example Usage

curl -X GET "https://your-api.com/oauth/callback"

Response:
Upon success, the user is redirected to:
https://your-frontend.com/dashboard?access_token=JWT_ACCESS_TOKEN&refresh_token=JWT_REFRESH_TOKEN
✅ JWT Tokens are generated and included in the redirect URL.

3️⃣ User Logout
GET /oauth/logout
Clears session data and logs the user out.

🔹 Request

Method: GET

URL: /oauth/logout

Headers: No authentication required.

🔹 Response
|Status Code|	Description|
|-------------|-------------|
|302 Found|	Redirects to the index page.|

🔹 Example Usage
curl -X GET "https://your-api.com/oauth/logout"

Response:
The user is redirected to:
https://your-api.com/index
