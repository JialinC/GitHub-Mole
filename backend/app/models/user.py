from app.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    github_token = db.Column(db.String(255), nullable=False)
    github_data = db.relationship('GitHubUserData', backref='user', lazy='dynamic')