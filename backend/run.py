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
            # Fetch all table names from the database
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()"))
            tables = [row[0] for row in result.fetchall()]
            return f"Successfully connected to MySQL database. Tables: {', '.join(tables)}"
    except Exception as e:
        # If an error occurs, it means the connection was unsuccessful
        return f"Failed to connect to database. Error: {e}"


if __name__ == "__main__":
    print("Accessible endpoints:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
    app.run(host="0.0.0.0", port=5000, debug=True)
