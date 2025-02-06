"""The module defines the User class, which users can utilize to mine GitHub users' contribution metrics."""

from app.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(
        db.String(80), unique=True, nullable=False
    )  # github user node_id
    github_login = db.Column(db.String(80), unique=True, nullable=False)
    personal_access_token = db.Column(db.String(255), nullable=False)
    api_url = db.Column(db.String(255), nullable=True)

    queries = db.relationship(
        "UserQuery", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.github_id}>"

    @classmethod
    def create(
        cls, github_id: str, github_login: str, personal_access_token: str, api_url: str
    ) -> "User":
        user = cls(
            github_id=github_id,
            github_login=github_login,
            personal_access_token=personal_access_token,
            api_url=api_url,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def read(cls, value: str) -> "User":
        return cls.query.filter_by(github_login=value).first()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
