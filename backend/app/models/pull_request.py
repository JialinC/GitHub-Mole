from app.database import db


class PullRequest(db.Model):
    __tablename__ = "pull_requests"

    id = db.Column(db.Integer, primary_key=True)
    pull_request_id = db.Column(db.String(80), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id"), nullable=False
    )

    def __repr__(self):
        return f"<PullRequest {self.pull_request_id}>"

    @classmethod
    def create(
        cls, pull_request_id, body_text, created_at, author_github_login, user_query_id
    ):
        pull_request = cls(
            pull_request_id=pull_request_id,
            body_text=body_text,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        db.session.add(pull_request)
        db.session.commit()
        return pull_request

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
