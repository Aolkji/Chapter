from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import db, Book

books = Blueprint("books", __name__, url_prefix="/books")


def read_book_form():
    """Pull the book fields out of the submitted form and check them."""
    data = {
        "title": request.form.get("title", "").strip(),
        "author": request.form.get("author", "").strip(),
        "genre": request.form.get("genre", "").strip() or None,
        "cover_image": request.form.get("cover_image", "").strip() or None,
    }

    errors = []
    if not data["title"]:
        errors.append("Title is required.")
    if not data["author"]:
        errors.append("Author is required.")

    return data, errors


# CREATE: show the form (GET) and save a new book (POST)
@books.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method == "POST":
        data, errors = read_book_form()

        if errors:
            for error in errors:
                flash(error, "error")
            # Re-show the form with what they already typed
            return render_template("book_form.html", book=data, mode="add")

        book = Book(**data)
        db.session.add(book)
        db.session.commit()

        flash(f'"{book.title}" was added.', "success")
        return redirect(url_for("books.book_detail", book_id=book.id))

    return render_template("book_form.html", book={}, mode="add")


# READ: one book's detail page
@books.route("/<int:book_id>")
def book_detail(book_id):
    book = db.get_or_404(Book, book_id)
    return render_template("book_detail.html", book=book)


# UPDATE: show the form filled in (GET) and save changes (POST)
@books.route("/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    book = db.get_or_404(Book, book_id)

    if request.method == "POST":
        data, errors = read_book_form()

        if errors:
            for error in errors:
                flash(error, "error")
            data["id"] = book.id
            return render_template("book_form.html", book=data, mode="edit")

        for field, value in data.items():
            setattr(book, field, value)
        db.session.commit()

        flash(f'"{book.title}" was updated.', "success")
        return redirect(url_for("books.book_detail", book_id=book.id))

    return render_template("book_form.html", book=book, mode="edit")


# DELETE: POST only, so a link click or page visit can't delete a book
@books.route("/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id):
    book = db.get_or_404(Book, book_id)
    title = book.title

    db.session.delete(book)
    db.session.commit()

    flash(f'"{title}" was deleted.', "success")
    return redirect(url_for("main.index"))