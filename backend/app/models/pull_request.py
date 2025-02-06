from app.database import db
from datetime import datetime


class PullRequest(db.Model):
    __tablename__ = "pull_requests"

    id = db.Column(db.Integer, primary_key=True)
    author_github_login = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    body_text = db.Column(db.Text, nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<PullRequest {self.body_text}>"

    @classmethod
    def create(cls, author_github_login, created_at, body_text, user_query_id):
        pull_request = cls(
            author_github_login=author_github_login,
            created_at=created_at,
            body_text=body_text,
            user_query_id=user_query_id,
        )
        return pull_request

    @classmethod
    def create_from_row(cls, row, user_query_id):
        created_at = (
            None
            if row.get("Created At") == "N/A"
            else datetime.strptime(row.get("Created At"), "%Y-%m-%dT%H:%M:%SZ")
        )
        return cls(
            body_text=row.get("Body Text"),
            created_at=created_at,
            author_github_login=row.get("GitHub ID"),
            user_query_id=user_query_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "body_text": self.body_text,
            "created_at": self.created_at.isoformat() if self.created_at else "N/A",
            "author_github_login": self.author_github_login,
            "user_query_id": self.user_query_id,
        }

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        pull_request = cls.query.get(id)
        if pull_request:
            for key, value in kwargs.items():
                setattr(pull_request, key, value)
            db.session.commit()
        return pull_request

    @classmethod
    def delete(cls, id):
        pull_request = cls.query.get(id)
        if pull_request:
            db.session.delete(pull_request)
            db.session.commit()
        return pull_request

    @classmethod
    def get_by_author_github_login(cls, author_github_login):
        return cls.query.filter_by(author_github_login=author_github_login).all()

    @classmethod
    def get_by_user_query_id(cls, user_query_id):
        return cls.query.filter_by(user_query_id=user_query_id).all()
