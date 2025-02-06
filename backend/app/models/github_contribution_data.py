from app.database import db
from datetime import datetime


class GithubContributionData(db.Model):
    __tablename__ = "github_contribution_data"

    id = db.Column(db.Integer, primary_key=True)
    author_github_login = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(80), nullable=False)
    watching = db.Column(db.Integer, nullable=False)
    starred_repo = db.Column(db.Integer, nullable=False)
    following = db.Column(db.Integer, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    private_contrib = db.Column(db.Integer, nullable=False)
    commits = db.Column(db.Integer, nullable=False)
    gists = db.Column(db.Integer, nullable=False)
    issues = db.Column(db.Integer, nullable=False)
    projects = db.Column(db.Integer, nullable=False)
    pull_requests = db.Column(db.Integer, nullable=False)
    pull_request_reviews = db.Column(db.Integer, nullable=False)
    repositories = db.Column(db.Integer, nullable=False)
    repo_discussions = db.Column(db.Integer, nullable=False)
    commit_comments = db.Column(db.Integer, nullable=False)
    issue_comments = db.Column(db.Integer, nullable=False)
    gist_comments = db.Column(db.Integer, nullable=False)
    repo_discussion_comments = db.Column(db.Integer, nullable=False)
    selected_langs = db.Column(db.Text, nullable=False)
    owned_original_repo = db.Column(db.Integer, nullable=False)
    owned_original_repo_size = db.Column(db.Integer, nullable=False)
    owned_original_repo_selected_langs_size = db.Column(db.Integer, nullable=False)
    owned_original_repo_langs_number = db.Column(db.Integer, nullable=False)
    owned_forked_repo = db.Column(db.Integer, nullable=False)
    owned_forked_repo_size = db.Column(db.Integer, nullable=False)
    owned_forked_repo_selected_langs_size = db.Column(db.Integer, nullable=False)
    owned_forked_repo_langs_number = db.Column(db.Integer, nullable=False)
    collaborating_original_repo = db.Column(db.Integer, nullable=False)
    collaborating_original_repo_size = db.Column(db.Integer, nullable=False)
    collaborating_original_repo_selected_langs_size = db.Column(
        db.Integer, nullable=False
    )
    collaborating_original_repo_langs_number = db.Column(db.Integer, nullable=False)
    collaborating_forked_repo = db.Column(db.Integer, nullable=False)
    collaborating_forked_repo_size = db.Column(db.Integer, nullable=False)
    collaborating_forked_repo_selected_langs_size = db.Column(
        db.Integer, nullable=False
    )
    collaborating_forked_repo_langs_size_number = db.Column(db.Integer, nullable=False)
    total_langs_number = db.Column(db.Integer, nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<GithubContributionData {self.name}>"

    @classmethod
    def create_from_row(cls, row, selected_langs, user_query_id):
        created_at = datetime.strptime(row.get("Created At"), "%Y-%m-%dT%H:%M:%SZ")
        return cls(
            author_github_login=row.get("GitHub ID"),
            name=row.get("Name"),
            email=row.get("Email"),
            created_at=created_at,
            age=row.get("Age (days)"),
            bio=row.get("Bio"),
            company=row.get("Company"),
            watching=row.get("Watching"),
            starred_repo=row.get("Starred Repositories"),
            following=row.get("Following"),
            followers=row.get("Followers"),
            private_contrib=row.get("Private Contributions"),
            commits=row.get("Commits"),
            gists=row.get("Gists"),
            issues=row.get("Issues"),
            projects=row.get("Projects"),
            pull_requests=row.get("Pull Requests"),
            pull_request_reviews=row.get("Pull Request Reviews"),
            repositories=row.get("Repositories"),
            repo_discussions=row.get("Repository Discussions"),
            commit_comments=row.get("Commit Comments"),
            issue_comments=row.get("Issue Comments"),
            gist_comments=row.get("Gist Comments"),
            repo_discussion_comments=row.get("Repository Discussion Comments"),
            selected_langs=selected_langs,
            owned_original_repo=row.get("Owned Original Repo"),
            owned_original_repo_size=row.get("Owned Original Repo Size"),
            owned_original_repo_selected_langs_size=row.get(
                "Owned Original Repo Selected Langs Size"
            ),
            owned_original_repo_langs_number=row.get(
                "Owned Original Repo Langs Number"
            ),
            owned_forked_repo=row.get("Owned Forked Repo"),
            owned_forked_repo_size=row.get("Owned Forked Repo Size"),
            owned_forked_repo_selected_langs_size=row.get(
                "Owned Forked Repo Selected Langs Size"
            ),
            owned_forked_repo_langs_number=row.get("Owned Forked Repo Langs Number"),
            collaborating_original_repo=row.get("Collaborating Original Repo"),
            collaborating_original_repo_size=row.get(
                "Collaborating Original Repo Size"
            ),
            collaborating_original_repo_selected_langs_size=row.get(
                "Collaborating Original Repo Selected Langs Size"
            ),
            collaborating_original_repo_langs_number=row.get(
                "Collaborating Original Repo Langs Number"
            ),
            collaborating_forked_repo=row.get("Collaborating Forked Repo"),
            collaborating_forked_repo_size=row.get("Collaborating Forked Repo Size"),
            collaborating_forked_repo_selected_langs_size=row.get(
                "Collaborating Forked Repo Selected Langs Size"
            ),
            collaborating_forked_repo_langs_size_number=row.get(
                "Collaborating Forked Repo Langs Size Number"
            ),
            total_langs_number=row.get("Total Langs Number"),
            user_query_id=user_query_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "author_github_login": self.author_github_login,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "age": self.age,
            "bio": self.bio,
            "company": self.company,
            "watching": self.watching,
            "starred_repo": self.starred_repo,
            "following": self.following,
            "followers": self.followers,
            "private_contrib": self.private_contrib,
            "commits": self.commits,
            "gists": self.gists,
            "issues": self.issues,
            "projects": self.projects,
            "pull_requests": self.pull_requests,
            "pull_request_reviews": self.pull_request_reviews,
            "repositories": self.repositories,
            "repo_discussions": self.repo_discussions,
            "commit_comments": self.commit_comments,
            "issue_comments": self.issue_comments,
            "gist_comments": self.gist_comments,
            "repo_discussion_comments": self.repo_discussion_comments,
            "selected_langs": self.selected_langs,
            "owned_original_repo": self.owned_original_repo,
            "owned_original_repo_size": self.owned_original_repo_size,
            "owned_original_repo_selected_langs_size": self.owned_original_repo_selected_langs_size,
            "owned_original_repo_langs_number": self.owned_original_repo_langs_number,
            "owned_forked_repo": self.owned_forked_repo,
            "owned_forked_repo_size": self.owned_forked_repo_size,
            "owned_forked_repo_selected_langs_size": self.owned_forked_repo_selected_langs_size,
            "owned_forked_repo_langs_number": self.owned_forked_repo_langs_number,
            "collaborating_original_repo": self.collaborating_original_repo,
            "collaborating_original_repo_size": self.collaborating_original_repo_size,
            "collaborating_original_repo_selected_langs_size": self.collaborating_original_repo_selected_langs_size,
            "collaborating_original_repo_langs_number": self.collaborating_original_repo_langs_number,
            "collaborating_forked_repo": self.collaborating_forked_repo,
            "collaborating_forked_repo_size": self.collaborating_forked_repo_size,
            "collaborating_forked_repo_selected_langs_size": self.collaborating_forked_repo_selected_langs_size,
            "collaborating_forked_repo_langs_size_number": self.collaborating_forked_repo_langs_size_number,
            "total_langs_number": self.total_langs_number,
            "user_query_id": self.user_query_id,
        }
