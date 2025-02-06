from app.database import db
from datetime import datetime


class Gist(db.Model):
    __tablename__ = "gists"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    author_github_login = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<Gist {self.description}>"

    @classmethod
    def create(cls, description, created_at, author_github_login, user_query_id):
        gist = cls(
            description=description,
            created_at=created_at,
            author_github_login=author_github_login,
            user_query_id=user_query_id,
        )
        return gist

    @classmethod
    def create_from_row(cls, row, user_query_id):
        created_at = (
            None
            if row.get("Created At") == "N/A"
            else datetime.strptime(row.get("Created At"), "%Y-%m-%dT%H:%M:%SZ")
        )
        return cls(
            description=row.get("Description"),
            created_at=created_at,
            author_github_login=row.get("GitHub ID"),
            user_query_id=user_query_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else "N/A",
            "author_github_login": self.author_github_login,
            "user_query_id": self.user_query_id,
        }

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
