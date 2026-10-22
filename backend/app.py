import os
from flask import Flask
from dotenv import load_dotenv

from models import db
from routes.main_routes import main

# Load environment variables from .env file
load_dotenv()

# Paths to the frontend folders (relative to this file's folder, backend/)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")


def create_app():
    # Create the Flask app and point it at the frontend folders
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=os.path.join(FRONTEND_DIR, "templates"),
        static_folder=os.path.join(FRONTEND_DIR, "static"),
    )

    # Set the secret key for session management
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")

    # Create the instance folder if it doesn't exist before SQLite tries
    # to create the database in it
    os.makedirs(app.instance_path, exist_ok=True)

    # Build a default database path in the instance folder.
    # SQLAlchemy needs the "sqlite:///" prefix in front of a file path.
    default_db_path = os.path.join(app.instance_path, "chapterchat.db")
    default_db_uri = "sqlite:///" + default_db_path

    # Use DATABASE_URL if it exists, otherwise use the default SQLite file
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", default_db_uri)

    # Turns off the tracking feature
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register route blueprints (add auth, books, reviews, discussions here later)
    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)