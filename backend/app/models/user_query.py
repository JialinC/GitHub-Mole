from app.database import db


class UserQuery(db.Model):
    __tablename__ = "user_queries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    queried_github_login = db.Column(db.String(80), nullable=False)
    queried_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    commit_comments = db.relationship(
        "CommitComment",
        backref="user_query",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<UserQuery {self.user_id} queried {self.queried_github_id}>"

    @classmethod
    def create(cls, user_id, queried_github_id):
        user_query = cls(user_id=user_id, queried_github_id=queried_github_id)
        db.session.add(user_query)
        db.session.commit()
        return user_query

    @classmethod
    def read(cls, query_id):
        return cls.query.get(query_id)

    @classmethod
    def update(cls, query_id, **kwargs):
        user_query = cls.query.get(query_id)
        if user_query:
            for key, value in kwargs.items():
                setattr(user_query, key, value)
            db.session.commit()
        return user_query

    @classmethod
    def delete(cls, query_id):
        user_query = cls.query.get(query_id)
        if user_query:
            db.session.delete(user_query)
            db.session.commit()
        return user_query

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_github_id(cls, queried_github_id):
        return cls.query.filter_by(queried_github_id=queried_github_id).all()
