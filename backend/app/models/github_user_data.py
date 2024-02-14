from datetime import datetime
from app.database import db

class GitHubUserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    github_login = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lifetime = db.Column(db.Integer)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    period = db.Column(db.Integer)

    private_contributions = db.Column(db.Integer)
    commits = db.Column(db.Integer)
    issues = db.Column(db.Integer)
    gists = db.Column(db.Integer)
    prs = db.Column(db.Integer)
    pr_reviews = db.Column(db.Integer)
    repository_discussions = db.Column(db.Integer)
    commit_comments = db.Column(db.Integer)
    issue_comments = db.Column(db.Integer)
    gist_comments = db.Column(db.Integer)
    repository_discussion_comments = db.Column(db.Integer)
    repos = db.Column(db.Integer)

    a_count = db.Column(db.Integer)
    a_fork_count = db.Column(db.Integer)
    a_stargazer_count = db.Column(db.Integer)
    a_watcher_count = db.Column(db.Integer)
    a_total_size = db.Column(db.BigInteger)
    a_langs = db.Column(db.Integer)

    b_count = db.Column(db.Integer)
    b_fork_count = db.Column(db.Integer)
    b_stargazer_count = db.Column(db.Integer)
    b_watcher_count = db.Column(db.Integer)
    b_total_size = db.Column(db.BigInteger)
    b_langs = db.Column(db.Integer)

    c_total_count = db.Column(db.Integer)
    c_fork_count = db.Column(db.Integer)
    c_stargazer_count = db.Column(db.Integer)
    c_watcher_count = db.Column(db.Integer)
    c_total_size = db.Column(db.BigInteger)
    c_langs = db.Column(db.Integer)

    d_total_count = db.Column(db.Integer)
    d_fork_count = db.Column(db.Integer)
    d_stargazer_count = db.Column(db.Integer)
    d_watcher_count = db.Column(db.Integer)
    d_total_size = db.Column(db.BigInteger)
    d_langs = db.Column(db.Integer)

    # Convert object properties to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'github_login': self.github_login,
            'semester': self.semester,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'lifetime': self.lifetime,
            'start_at': self.start_at.isoformat() if self.start_at else None,
            'end_at': self.end_at.isoformat() if self.end_at else None,
            'period': self.period,

            'private_contributions': self.private_contributions,
            'commits': self.commits,
            'issues': self.issues,
            'gists': self.gists,
            'prs': self.prs,
            'pr_reviews': self.pr_reviews,
            'repository_discussions': self.repository_discussions,
            'commit_comments': self.commit_comments,
            'issue_comments': self.issue_comments,
            'gist_comments': self.gist_comments,
            'repository_discussion_comments': self.repository_discussion_comments,
            'repos': self.repos,

            'a_count': self.a_count,
            'a_fork_count': self.a_fork_count,
            'a_stargazer_count': self.a_stargazer_count,
            'a_watcher_count': self.a_watcher_count,
            'a_total_size': self.a_total_size,
            'a_langs': self.a_langs,

            'b_count': self.b_count,
            'b_fork_count': self.b_fork_count,
            'b_stargazer_count': self.b_stargazer_count,
            'b_watcher_count': self.b_watcher_count,
            'b_total_size': self.b_total_size,
            'b_langs': self.b_langs,

            'c_total_count': self.c_total_count,
            'c_fork_count': self.c_fork_count,
            'c_stargazer_count': self.c_stargazer_count,
            'c_watcher_count': self.c_watcher_count,
            'c_total_size': self.c_total_size,
            'c_langs': self.c_langs,

            'd_total_count': self.d_total_count,
            'd_fork_count': self.d_fork_count,
            'd_stargazer_count': self.d_stargazer_count,
            'd_watcher_count': self.d_watcher_count,
            'd_total_size': self.d_total_size,
            'd_langs': self.d_langs,
        }