from app.database import db


class IssueComment(db.Model):
    __tablename__ = "issue_comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(80), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id"), nullable=False
    )

    def __repr__(self):
        return f"<IssueComment {self.comment_id}>"

    @classmethod
    def create(
        cls, comment_id, body_text, created_at, author_github_login, user_query_id
    ):
        issue_comment = cls(
            comment_id=comment_id,
            body_text=body_text,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        db.session.add(issue_comment)
        db.session.commit()
        return issue_comment

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
