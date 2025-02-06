from app.database import db
from datetime import datetime


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    author_github_login = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    body_text = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<Issue {self.title} {self.body_text}>"

    @classmethod
    def create(cls, author_github_login, created_at, body_text, title, user_query_id):
        issue = cls(
            author_github_login=author_github_login,
            created_at=created_at,
            body_text=body_text,
            title=title,
            user_query_id=user_query_id,
        )
        return issue

    @classmethod
    def create_from_row(cls, row, user_query_id):
        created_at = (
            None
            if row.get("Created At") == "N/A"
            else datetime.strptime(row.get("Created At"), "%Y-%m-%dT%H:%M:%SZ")
        )
        return cls(
            author_github_login=row.get("GitHub ID"),
            created_at=created_at,
            body_text=row.get("Body Text"),
            title=row.get("Title"),
            user_query_id=user_query_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "author_github_login": self.author_github_login,
            "created_at": self.created_at.isoformat() if self.created_at else "N/A",
            "body_text": self.body_text,
            "title": self.title,
            "user_query_id": self.user_query_id,
        }

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        issue = cls.query.get(id)
        if issue:
            for key, value in kwargs.items():
                setattr(issue, key, value)
            db.session.commit()
        return issue

    @classmethod
    def delete(cls, id):
        issue = cls.query.get(id)
        if issue:
            db.session.delete(issue)
            db.session.commit()
        return issue

    @classmethod
    def get_by_author_github_login(cls, author_github_login):
        return cls.query.filter_by(author_github_login=author_github_login).all()

    @classmethod
    def get_by_user_query_id(cls, user_query_id):
        return cls.query.filter_by(user_query_id=user_query_id).all()
