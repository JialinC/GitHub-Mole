from app.database import db


class Repository(db.Model):
    __tablename__ = "repositories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    repository_id = db.Column(db.String(80), nullable=False)
    owner_id = db.Column(db.String(80), nullable=False)
    affiliation_login = db.Column(db.String(80), nullable=False)
    repository_type = db.Column(db.String(80), nullable=False)
    primary_language_id = db.Column(
        db.Integer, db.ForeignKey("languages.id"), nullable=True
    )

    primary_language = db.relationship(
        "Language", backref="primary_repositories", foreign_keys=[primary_language_id]
    )
    languages = db.relationship(
        "Language", secondary="repository_languages", backref="repositories"
    )

    def __repr__(self):
        return f"<Repository {self.name}>"

    @classmethod
    def create(
        cls,
        name,
        created_at,
        updated_at,
        repository_id,
        owner_id,
        affiliation_login,
        repository_type,
        primary_language_id=None,
    ):
        repository = cls(
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            repository_id=repository_id,
            owner_id=owner_id,
            affiliation_login=affiliation_login,
            repository_type=repository_type,
            primary_language_id=primary_language_id,
        )
        db.session.add(repository)
        db.session.commit()
        return repository

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
