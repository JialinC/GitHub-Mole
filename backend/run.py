from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)





from flask import Flask, jsonify, request
from flask_cors import CORS
import os
# G2370
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client
from github_query.queries.comments.user_commit_comments import UserCommitComments
from github_query.queries.comments.user_gist_comments import UserGistComments
from github_query.queries.comments.user_issue_comments import UserIssueComments
from github_query.queries.comments.user_repository_discussion_comments import UserRepositoryDiscussionComments
from github_query.queries.profile.user_login import UserLogin
from github_query.queries.profile.user_profile_stats import UserProfileStats
from github_query.queries.time_range_contributions.user_contributions_collection import UserContributionsCollection
# G2371
from github_query.model.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.github_client import GitHubClient
from github_query.queries.contributions.user_login import UserLogin
from flask_server.service.paginated_service import PaginatedService
# G2372
from github_query.github_graphql.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.client import Client
from github_query.queries.repositories.user_login import UserLogin
from github_query.queries.repositories.repository_commits import RepositoryCommits
from github_query.queries.repositories.repository_contributors_contribution import RepositoryContributorsContribution
from github_query.queries.repositories.repository_contributors import RepositoryContributors



app = Flask(__name__)

# Allow all origins to access routes with '/api/' prefix
CORS(app, resources={r"/api/*": {"origins": "*"}})

auth_token = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

# Initialize GitHub client
client = Client(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=auth_token)
)

@app.route('/api/github/userlogin')
def fetch_github_data():
    user_name = request.args.get("user")
    response = client.execute(
        query=UserLogin(), substitutions={"user": user_name}
    )
    return response

@app.route('/api/github/commitcomments')
def fetch_commit_comments():
    account_name = request.args.get("account_name")
    page_size = request.args.get("page_size")
    response = client.execute(
        query=UserCommitComments(), 
        substitutions={"user": account_name, "pg_size": page_size})
    commit_comments = []
    for commitComments in response:
        commit_comments.append(commitComments)

    return commit_comments

@app.route('/api/github/gistcomments')
def fetch_gist_comments():
    account_name = request.args.get("account_name")
    page_size = request.args.get("page_size")
    response = client.execute(
        query=UserGistComments(), 
        substitutions={"user": account_name, "pg_size": page_size})
    gist_comments = []
    for gistComments in response:
        gist_comments.append(gistComments)

    return gist_comments

@app.route('/api/github/issuecomments')
def fetch_issue_comments():
    account_name = request.args.get("account_name")
    page_size = request.args.get("page_size")
    response = client.execute(
        query=UserIssueComments(), 
        substitutions={"user": account_name, "pg_size": page_size})
    issue_comments = []
    for issueComments in response:
        issue_comments.append(issueComments)

    return issue_comments


@app.route('/api/github/repodiscussion')
def fetch_user_repo_discussions():
    account_name = request.args.get("account_name")
    page_size = request.args.get("page_size")
    response = client.execute(query=UserRepositoryDiscussionComments(),
                              substitutions={"user": account_name, "pg_size": page_size})
    repo_discussions = []
    for discussion in response:
        repo_discussions.append(discussion)

    return repo_discussions


@app.route('/api/github/profilestats')
def fetch_user_profile_stats():
    account_name = request.args.get("account_name")
    response = client.execute(query=UserProfileStats(),
                              substitutions={"user": account_name})
    return UserProfileStats.profile_stats(response)


@app.route('/api/github/contributioncollection')
def fetch_user_contribution_collection():
    account_name = request.args.get("account_name")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    # "start": "2023-09-07T18:11:20Z"
    # "end": "2023-10-17T18:11:20Z"
    response = client.execute(query=UserContributionsCollection(), substitutions={"user": account_name,
                                                                                  "start": start_date,
                                                                                  "end": end_date})
    return response


# Run the app on 0.0.0.0
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1234)