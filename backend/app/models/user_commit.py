from app.database import db

user_commit = db.Table(
    "user_commit",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column(
        "commit_id",
        db.String(255),
        db.ForeignKey("commits.commit_id"),
        primary_key=True,
    ),
)
