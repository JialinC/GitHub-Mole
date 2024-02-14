from app import create_app
from app.database import db
from sqlalchemy import text
from flask import Flask, session, jsonify, request, abort
from app.models.user import User
from app.models.github_user_data import GitHubUserData
from datetime import datetime, timedelta

app = create_app()

@app.route('/index')
def index():
    return 'This is the index page'

@app.route('/show_session')
def show_session():
    # Print all session data to the console
    for key, value in session.items():
        print(f'{key}: {value}')
    
    return 'Session data printed to console.'

@app.route('/test_db')
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT VERSION()'))
            version = result.fetchone()[0]
            return f'Successfully connected to MySQL database. Version: {version}'
    except Exception as e:
        # If an error occurs, it means the connection was unsuccessful
        return f'Failed to connect to database. Error: {e}'

@app.route('/test-insert/<int:user_id>/<login>')
def test_insert(user_id, login):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    # Create GitHubUserData instances with all fields
    gh_data = GitHubUserData(
        user_id=user.id, github_login=login, semester='2023 Spring', created_at=datetime.utcnow(),
        lifetime=100, start_at=datetime.utcnow() - timedelta(days=30), end_at=datetime.utcnow(),
        period=30, private_contributions=10, commits=100, issues=10, gists=1, prs=5, pr_reviews=2,
        repository_discussions=0, commit_comments=3, issue_comments=4, gist_comments=0,
        repository_discussion_comments=0, repos=2, a_count=1, a_fork_count=0, a_stargazer_count=5,
        a_watcher_count=10, a_total_size=2048, a_langs=2, b_count=0, b_fork_count=0, 
        b_stargazer_count=0, b_watcher_count=0, b_total_size=0, b_langs=0, c_total_count=1,
        c_fork_count=0,c_stargazer_count=3,c_watcher_count=2,c_total_size=1024,c_langs=1,
        d_total_count=1,d_fork_count=0,d_stargazer_count=2,d_watcher_count=1,d_total_size=512,d_langs=1
    )

    try:
        db.session.add(gh_data)
        db.session.commit()
        return jsonify({'message': 'User added successfully', 'username': user.username, 'email': user.email}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/test-retrive/<int:user_id>')
def get_github_data(user_id):
    try:
        # Query GitHubUserData based on user_id
        github_data = GitHubUserData.query.filter_by(user_id=user_id).all()

        # Check if data exists for the user
        if not github_data:
            return jsonify({"error": "No data found for the given user ID"}), 404

        # Convert the data to a list of dictionaries for JSON serialization
        data_list = [data.to_dict() for data in github_data]  # Assuming you have a to_dict method

        return jsonify(data_list)

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
