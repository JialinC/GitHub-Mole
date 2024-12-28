from app.database import db


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.String(80), nullable=False)
    title = db.Column(db.Text, nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id"), nullable=False
    )

    def __repr__(self):
        return f"<Issue {self.issue_id}>"

    @classmethod
    def create(
        cls, issue_id, title, body_text, created_at, author_github_login, user_query_id
    ):
        issue = cls(
            issue_id=issue_id,
            title=title,
            body_text=body_text,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        db.session.add(issue)
        db.session.commit()
        return issue

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
