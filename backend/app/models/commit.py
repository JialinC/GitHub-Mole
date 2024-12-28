from app.database import db
from .user_commit import user_commit


class Commit(db.Model):
    __tablename__ = "commits"

    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.String(255), nullable=False, unique=True)
    authored_date = db.Column(db.DateTime, nullable=False)
    changed_files = db.Column(db.Integer, nullable=True)
    additions = db.Column(db.Integer, nullable=True)
    deletions = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text, nullable=True)
    author_name = db.Column(db.String(80), nullable=True)
    author_email = db.Column(db.String(80), nullable=True)
    author_login = db.Column(db.String(80), nullable=True)
    repo_owner_login = db.Column(db.String(80), nullable=True)
    repo_name = db.Column(db.String(80), nullable=True)

    users = db.relationship("User", secondary=user_commit, backref="commits")

    def __repr__(self):
        return f"<Commit {self.commit_id}>"

    @classmethod
    def create(
        cls,
        commit_id,
        authored_date,
        changed_files,
        additions,
        deletions,
        repository_id,
        author_email=None,
        author_login=None,
        repo_owner_login=None,
        repo_name=None,
        user_ids=[],
    ):
        commit = cls(
            commit_id=commit_id,
            authored_date=authored_date,
            changed_files=changed_files,
            additions=additions,
            deletions=deletions,
            repository_id=repository_id,
            author_email=author_email,
            author_login=author_login,
            repo_owner_login=repo_owner_login,
            repo_name=repo_name,
        )
        db.session.add(commit)
        db.session.commit()

        # Add users to the commit
        # for user_id in user_ids:
        #     user = User.query.get(user_id)
        #     if user:
        #         commit.users.append(user)
        # db.session.commit()

        return commit

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        commit = cls.query.get(id)
        if commit:
            for key, value in kwargs.items():
                setattr(commit, key, value)
            db.session.commit()
        return commit

    @classmethod
    def delete(cls, id):
        commit = cls.query.get(id)
        if commit:
            db.session.delete(commit)
            db.session.commit()
        return commit

    @classmethod
    def get_by_commit_id(cls, commit_id):
        return cls.query.filter_by(commit_id=commit_id).first()
