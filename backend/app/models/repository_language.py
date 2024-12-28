from app.database import db

repository_languages = db.Table(
    "repository_languages",
    db.Column(
        "repository_id", db.Integer, db.ForeignKey("repositories.id"), primary_key=True
    ),
    db.Column(
        "language_id", db.Integer, db.ForeignKey("languages.id"), primary_key=True
    ),
    db.Column("size", db.Integer, nullable=False),
)
