from flask import Blueprint, render_template
 
from models import Book
 
main = Blueprint("main", __name__)
 
 
@main.route("/")
def index():
    # Query all books from the database
    books = Book.query.all()
    return render_template("index.html", books=books)