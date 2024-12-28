from app.database import db


class Gist(db.Model):
    __tablename__ = "gists"

    id = db.Column(db.Integer, primary_key=True)
    gist_id = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id"), nullable=False
    )

    def __repr__(self):
        return f"<Gist {self.gist_id}>"

    @classmethod
    def create(
        cls, gist_id, description, created_at, author_github_login, user_query_id
    ):
        gist = cls(
            gist_id=gist_id,
            description=description,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        db.session.add(gist)
        db.session.commit()
        return gist

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        gist = cls.query.get(id)
        if gist:
            for key, value in kwargs.items():
                setattr(gist, key, value)
            db.session.commit()
        return gist

    @classmethod
    def delete(cls, id):
        gist = cls.query.get(id)
        if gist:
            db.session.delete(gist)
            db.session.commit()
        return gist

    @classmethod
    def get_by_author_github_login(cls, author_github_login):
        return cls.query.filter_by(author_github_login=author_github_login).all()

    @classmethod
    def get_by_user_query_id(cls, user_query_id):
        return cls.query.filter_by(user_query_id=user_query_id).all()
