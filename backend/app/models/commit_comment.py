from app.database import db
from datetime import datetime


class CommitComment(db.Model):
    __tablename__ = "commit_comments"

    id = db.Column(db.Integer, primary_key=True)
    body_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<CommitComment {self.body_text}>"

    @classmethod
    def create(cls, body_text, created_at, author_github_login, user_query_id):
        commit_comment = cls(
            body_text=body_text,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        db.session.add(commit_comment)
        return commit_comment

    @classmethod
    def create_from_row(cls, row, user_query_id):
        created_at = (
            None if row[1] == "N/A" else datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%SZ")
        )
        return cls(
            body_text=row[2],
            created_at=created_at,
            author_github_login=row[0],
            user_query_id=user_query_id,
        )

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        commit_comment = cls.query.get(id)
        if commit_comment:
            for key, value in kwargs.items():
                setattr(commit_comment, key, value)
            db.session.commit()
        return commit_comment

    @classmethod
    def delete(cls, id):
        commit_comment = cls.query.get(id)
        if commit_comment:
            db.session.delete(commit_comment)
            db.session.commit()
        return commit_comment

    @classmethod
    def get_by_author_github_login(cls, author_github_login):
        return cls.query.filter_by(author_github_login=author_github_login).all()

    @classmethod
    def get_by_user_query_id(cls, user_query_id):
        return cls.query.filter_by(user_query_id=user_query_id).all()
