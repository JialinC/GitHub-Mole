from app.database import db


class RepositoryDiscussion(db.Model):
    __tablename__ = "repository_discussions"

    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.String(80), nullable=False)
    body_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id"), nullable=False
    )

    def __repr__(self):
        return f"<RepositoryDiscussion {self.discussion_id}>"

    @classmethod
    def create(
        cls, discussion_id, body_text, created_at, author_github_login, user_query_id
    ):
        discussion = cls(
            discussion_id=discussion_id,
            body_text=body_text,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        db.session.add(discussion)
        db.session.commit()
        return discussion

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        discussion = cls.query.get(id)
        if discussion:
            for key, value in kwargs.items():
                setattr(discussion, key, value)
            db.session.commit()
        return discussion

    @classmethod
    def delete(cls, id):
        discussion = cls.query.get(id)
        if discussion:
            db.session.delete(discussion)
            db.session.commit()
        return discussion

    @classmethod
    def get_by_author_github_login(cls, author_github_login):
        return cls.query.filter_by(author_github_login=author_github_login).all()

    @classmethod
    def get_by_user_query_id(cls, user_query_id):
        return cls.query.filter_by(user_query_id=user_query_id).all()
