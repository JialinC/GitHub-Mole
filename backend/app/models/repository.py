from app.database import db
from datetime import datetime


class Repository(db.Model):
    __tablename__ = "repositories"

    id = db.Column(db.Integer, primary_key=True)
    author_github_login = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    primary_language = db.Column(db.String(80), nullable=False)
    languages = db.Column(db.Text, nullable=False)
    repository_type = db.Column(db.String(80), nullable=False)
    user_query_id = db.Column(
        db.Integer, db.ForeignKey("user_queries.id", ondelete="CASCADE"), nullable=False
    )

    def __repr__(self):
        return f"<Repository {self.repository_type} {self.name}>"

    @classmethod
    def create(
        cls,
        author_github_login,
        name,
        created_at,
        updated_at,
        primary_language,
        languages,
        repository_type,
        user_query_id,
    ):
        repository = cls(
            author_github_login=author_github_login,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            primary_language=primary_language,
            languages=languages,
            repository_type=repository_type,
            user_query_id=user_query_id,
        )
        return repository

    @classmethod
    def create_from_row(cls, row, repository_type, user_query_id):
        created_at = (
            None
            if row.get("Created At") == "N/A"
            else datetime.strptime(row.get("Created At"), "%Y-%m-%dT%H:%M:%SZ")
        )
        updated_at = (
            None
            if row.get("Updated At") == "N/A"
            else datetime.strptime(row.get("Updated At"), "%Y-%m-%dT%H:%M:%SZ")
        )

        return cls(
            author_github_login=row.get("GitHub ID"),
            name=row.get("Name"),
            created_at=created_at,
            updated_at=updated_at,
            primary_language=row.get("Primary Language"),
            languages=row.get("Language Stats"),
            repository_type=repository_type,
            user_query_id=user_query_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "author_github_login": self.author_github_login,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else "N/A",
            "updated_at": self.updated_at.isoformat() if self.updated_at else "N/A",
            "primary_language": self.primary_language,
            "languages": self.languages,
            "repository_type": self.repository_type,
            "user_query_id": self.user_query_id,
        }

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        repository = cls.query.get(id)
        if repository:
            for key, value in kwargs.items():
                setattr(repository, key, value)
            db.session.commit()
        return repository

    @classmethod
    def delete(cls, id):
        repository = cls.query.get(id)
        if repository:
            db.session.delete(repository)
            db.session.commit()
        return repository

    @classmethod
    def get_by_affiliation_login(cls, affiliation_login):
        return cls.query.filter_by(affiliation_login=affiliation_login).all()

    @classmethod
    def get_by_repository_id(cls, repository_id):
        return cls.query.filter_by(repository_id=repository_id).all()
