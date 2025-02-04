from app.database import db
from datetime import datetime


class IssueComment(db.Model):
    __tablename__ = "issue_comments"

    id = db.Column(db.Integer, primary_key=True)
    body_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<IssueComment {self.body_text}>"

    @classmethod
    def create(cls, body_text, created_at, author_github_login, user_query_id):
        issue_comment = cls(
            body_text=body_text,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        return issue_comment

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
        issue_comment = cls.query.get(id)
        if issue_comment:
            for key, value in kwargs.items():
                setattr(issue_comment, key, value)
            db.session.commit()
        return issue_comment

    @classmethod
    def delete(cls, id):
        issue_comment = cls.query.get(id)
        if issue_comment:
            db.session.delete(issue_comment)
            db.session.commit()
        return issue_comment

    @classmethod
    def get_by_author_github_login(cls, author_github_login):
        return cls.query.filter_by(author_github_login=author_github_login).all()

    @classmethod
    def get_by_user_query_id(cls, user_query_id):
        return cls.query.filter_by(user_query_id=user_query_id).all()
