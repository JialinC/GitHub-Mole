from app.database import db


class UserQuery(db.Model):
    __tablename__ = "user_queries"

    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(
        db.String(80), db.ForeignKey("users.github_login"), nullable=False
    )
    ds_name = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    queried_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    data_type = db.Column(db.String(80), nullable=False)  # Add this line

    total_contribution = db.relationship(
        "GithubContributionData",
        backref="user_query",
        lazy=True,
        cascade="all, delete-orphan",
    )
    commit_comments = db.relationship(
        "CommitComment", backref="user_query", lazy=True, cascade="all, delete-orphan"
    )
    issue_comments = db.relationship(
        "IssueComment", backref="user_query", lazy=True, cascade="all, delete-orphan"
    )
    gist_comments = db.relationship(
        "GistComment", backref="user_query", lazy=True, cascade="all, delete-orphan"
    )
    repository_discussion_comments = db.relationship(
        "RepositoryDiscussionComment",
        backref="user_query",
        lazy=True,
        cascade="all, delete-orphan",
    )
    gists = db.relationship(
        "Gist", backref="user_query", lazy=True, cascade="all, delete-orphan"
    )
    issues = db.relationship(
        "Issue", backref="user_query", lazy=True, cascade="all, delete-orphan"
    )
    pull_requests = db.relationship(
        "PullRequest", backref="user_query", lazy=True, cascade="all, delete-orphan"
    )
    repository_discussion = db.relationship(
        "RepositoryDiscussion",
        backref="user_query",
        lazy=True,
        cascade="all, delete-orphan",
    )
    repository = db.relationship(
        "Repository",
        backref="user_query",
        lazy=True,
        cascade="all, delete-orphan",
    )
    commit = db.relationship(
        "Commit",
        backref="user_query",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<UserQuery {self.user_login} queried {self.ds_name} for {self.data_type}>"
        )

    @classmethod
    def create(cls, user_login, ds_name, start_time, end_time, data_type):
        user_query = cls(
            user_login=user_login,
            ds_name=ds_name,
            start_time=start_time,
            end_time=end_time,
            data_type=data_type,
        )
        db.session.add(user_query)
        return user_query

    def to_dict(self):
        return {
            "id": self.id,
            "user_login": self.user_login,
            "ds_name": self.ds_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "queried_at": self.queried_at,
            "data_type": self.data_type,
        }

    @classmethod
    def read(cls, query_id):
        return cls.query.get(query_id)

    @classmethod
    def update(cls, query_id, **kwargs):
        user_query = cls.query.get(query_id)
        if user_query:
            for key, value in kwargs.items():
                setattr(user_query, key, value)
        return user_query

    @classmethod
    def delete(cls, query_id):
        user_query = cls.query.get(query_id)
        if user_query:
            db.session.delete(user_query)
        return user_query

    @classmethod
    def get_by_user_login(cls, user_login):
        return cls.query.filter_by(user_login=user_login).all()

    @classmethod
    def get_by_name(cls, user_login, name):
        return cls.query.filter_by(user_login=user_login, name=name).all()
