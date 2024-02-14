from app import create_app
from app.database import db
from app.models.user import User
from app.models.github_user_data import GitHubUserData
from datetime import datetime, timedelta


def seed_database():
    # Clear existing data
    db.session.query(GitHubUserData).delete()
    db.session.query(User).delete()

    # Create new users
    user1 = User(username='user1', email='user1@example.com', github_token='token1')
    user2 = User(username='user2', email='user2@example.com', github_token='token2')

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)

    # Commit to save users and to assign them IDs
    db.session.commit()

    # Create GitHubUserData instances with all fields
    gh_data1 = GitHubUserData(
        user_id=user1.id,
        github_login='ghuser1',
        semester='2023 Spring',
        created_at=datetime.utcnow(),
        lifetime=100,
        start_at=datetime.utcnow() - timedelta(days=30),
        end_at=datetime.utcnow(),
        period=30,
        private_contributions=10,
        commits=100,
        issues=10,
        gists=1,
        prs=5,
        pr_reviews=2,
        repository_discussions=0,
        commit_comments=3,
        issue_comments=4,
        gist_comments=0,
        repository_discussion_comments=0,
        repos=2,
        a_count=1,
        a_fork_count=0,
        a_stargazer_count=5,
        a_watcher_count=10,
        a_total_size=2048,
        a_langs=2,
        b_count=0,
        b_fork_count=0,
        b_stargazer_count=0,
        b_watcher_count=0,
        b_total_size=0,
        b_langs=0,
        c_total_count=1,
        c_fork_count=0,
        c_stargazer_count=3,
        c_watcher_count=2,
        c_total_size=1024,
        c_langs=1,
        d_total_count=1,
        d_fork_count=0,
        d_stargazer_count=2,
        d_watcher_count=1,
        d_total_size=512,
        d_langs=1
    )

    gh_data2 = GitHubUserData(
        user_id=user2.id,
        github_login='ghuser2',
        semester='2023 Fall',
        created_at=datetime.utcnow(),
        lifetime=150,
        start_at=datetime.utcnow() - timedelta(days=60),
        end_at=datetime.utcnow(),
        period=60,
        private_contributions=20,
        commits=150,
        issues=15,
        gists=2,
        prs=7,
        pr_reviews=3,
        repository_discussions=1,
        commit_comments=5,
        issue_comments=6,
        gist_comments=1,
        repository_discussion_comments=1,
        repos=3,
        a_count=2,
        a_fork_count=1,
        a_stargazer_count=8,
        a_watcher_count=15,
        a_total_size=4096,
        a_langs=3,
        b_count=1,
        b_fork_count=0,
        b_stargazer_count=4,
        b_watcher_count=7,
        b_total_size=2048,
        b_langs=2,
        c_total_count=2,
        c_fork_count=1,
        c_stargazer_count=6,
        c_watcher_count=5,
        c_total_size=3072,
        c_langs=2,
        d_total_count=2,
        d_fork_count=1,
        d_stargazer_count=5,
        d_watcher_count=3,
        d_total_size=2048,
        d_langs=2
    )

    # Add GitHubUserData instances to the session
    db.session.add(gh_data1)
    db.session.add(gh_data2)

    # Commit to save GitHubUserData instances
    db.session.commit()

# Call the function to seed the database
if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()
    print("seed done")
