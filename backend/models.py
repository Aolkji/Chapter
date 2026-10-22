from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user -> many reviews / discussion posts
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    discussions = db.relationship("Discussion", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        # Store a hash, never the plain password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(80))
    cover_image = db.Column(db.String(500))  # URL (e.g. from Google Books API)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One book -> many reviews / discussion posts
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete-orphan")
    discussions = db.relationship("Discussion", back_populates="book", cascade="all, delete-orphan")

    def average_rating(self):
        if not self.reviews:
            return None
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    book = db.relationship("Book", back_populates="reviews")

    # Keep ratings between 1 and 5 at the database level
    __table_args__ = (
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range"),
    )

    def __repr__(self):
        return f"<Review {self.rating}/5 book={self.book_id}>"


class Discussion(db.Model):
    __tablename__ = "discussions"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    # Self-referencing foreign key: NULL = top-level comment, otherwise a reply
    parent_id = db.Column(db.Integer, db.ForeignKey("discussions.id"), nullable=True)

    user = db.relationship("User", back_populates="discussions")
    book = db.relationship("Book", back_populates="discussions")
    replies = db.relationship(
        "Discussion",
        backref=db.backref("parent", remote_side=[id]),
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Discussion {self.id} parent={self.parent_id}>"