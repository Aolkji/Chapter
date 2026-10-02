import os 
from flask import Flask, render_template
from dotenv import load_dotenv

from models import db,Book

# Load environment variables from .env file
load_dotenv()

def create_app():
    # Create and configure the Flask application
    app = Flask(__name__, instance_relative_config=True)
    # Set the secret key for session management 
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")

    # Create the instance folder if it doesn't exist before SQLite tries
    # to create the database in it
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Build a default database path in the instance folder
    default_db_path = os.path.join(app.instance_path, "chapterchat.db")

    #Use the DATABASE_URL  if it exists, otherwise use the default path
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", default_db_path)

    #Turns off the tracking feature 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        # Query all books from the database
        books = Book.query.all()
        
        return render_template("index.html", books=books)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)