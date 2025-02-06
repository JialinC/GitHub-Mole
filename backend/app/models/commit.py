from app.database import db
from typing import Any, Dict
from datetime import datetime


class Commit(db.Model):
    __tablename__ = "commits"

    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(80), nullable=True)
    author_name = db.Column(db.String(80), nullable=True)
    author_email = db.Column(db.String(80), nullable=True)
    author_login = db.Column(db.String(80), nullable=True)
    branch = db.Column(db.String(80), nullable=True)
    authored_date = db.Column(db.DateTime, nullable=True)
    changed_files = db.Column(db.Integer, nullable=True)
    additions = db.Column(db.Integer, nullable=True)
    deletions = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text, nullable=True)
    parent_count = db.Column(db.Integer, nullable=True)
    lang_stats = db.Column(db.Text, nullable=True)

    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<Commit {self.message}>"

    @classmethod
    def create(cls, user_query_id: int, **kwargs: Any) -> "Commit":
        commit = cls(
            repo_name=kwargs.get("Repository"),
            author_name=kwargs.get("Author"),
            author_email=kwargs.get("Author Email"),
            author_login=kwargs.get("Author Login"),
            branch=kwargs.get("Branch"),
            authored_date=kwargs.get("Authored Date"),
            changed_files=kwargs.get("Changed Files"),
            additions=kwargs.get("Additions"),
            deletions=kwargs.get("Deletions"),
            message=kwargs.get("Message"),
            parent_count=kwargs.get("Parents"),
            lang_stats=kwargs.get("Language Stats"),
            user_query_id=user_query_id,
        )
        return commit

    @classmethod
    def create_from_row(cls, row: Dict[str, Any], user_query_id: int) -> "Commit":
        authored_date = (
            None
            if row.get("Authored Date") == "N/A"
            else datetime.strptime(row.get("Authored Date"), "%Y-%m-%dT%H:%M:%SZ")
        )
        return cls(
            repo_name=row.get("Repository"),
            author_name=row.get("Author"),
            author_email=row.get("Author Email"),
            author_login=row.get("Author Login"),
            branch=row.get("Branch"),
            authored_date=authored_date,
            changed_files=row.get("Changed Files"),
            additions=row.get("Additions"),
            deletions=row.get("Deletions"),
            message=row.get("Message"),
            parent_count=row.get("Parents"),
            lang_stats=row.get("Languages"),
            user_query_id=user_query_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "repo_name": self.repo_name,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "author_login": self.author_login,
            "branch": self.branch,
            "authored_date": (
                self.authored_date.isoformat() if self.authored_date else "N/A"
            ),
            "changed_files": self.changed_files,
            "additions": self.additions,
            "deletions": self.deletions,
            "message": self.message,
            "parent_count": self.parent_count,
            "lang_stats": self.lang_stats,
            "user_query_id": self.user_query_id,
        }

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        commit = cls.query.get(id)
        if commit:
            for key, value in kwargs.items():
                setattr(commit, key, value)
            db.session.commit()
        return commit

    @classmethod
    def delete(cls, id):
        commit = cls.query.get(id)
        if commit:
            db.session.delete(commit)
            db.session.commit()
        return commit

    @classmethod
    def get_by_commit_id(cls, commit_id):
        return cls.query.filter_by(commit_id=commit_id).first()
