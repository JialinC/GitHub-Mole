from app import create_app
from flask_cors import CORS
from app.database import db
from flask import session
from flask_jwt_extended import JWTManager
from sqlalchemy import text

app = create_app()
CORS(app)
jwt = JWTManager(app)


@app.route("/index")
def index():
    return "This is the index page"


@app.route("/show_session")
def show_session():
    # Print all session data to the console
    for key, value in session.items():
        print(f"{key}: {value}")

    return "Session data printed to console."


@app.route("/test_db")
def test_db():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            return f"Successfully connected to MySQL database. Version: {version}"
    except Exception as e:
        # If an error occurs, it means the connection was unsuccessful
        return f"Failed to connect to database. Error: {e}"
