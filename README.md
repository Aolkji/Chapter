# ChapterChat

A book club platform built around asynchronous discussion.

ChapterChat is built on the idea that book clubs shouldn't need to be online at the same time to talk about what they're reading. Where the usual workaround is a live call or a chat app's disappearing message feed, ChapterChat gives a book club one dedicated, asynchronous space: track what you're reading, rate and review it, and hold ongoing, threaded discussions that anyone can catch up on and contribute to whenever they have time — not just during a scheduled window.

## Inspirations

* TBD...

## Features

* **Books** — add, edit, and delete books (title, author, genre, cover image), with details auto-populated via the Google Books API
* **Reviews & Ratings** — rate a book 1–5 stars and leave a written review
* **Discussions** — threaded, nested comment discussions per book, so replies stay organized under the conversation they belong to
* **Users** — register, log in, and manage a profile

### Planned (post-MVP)

* Search/filter the book catalog by genre or rating
* Expanded profile pages (reading history, review activity)

## Tech Stack

### Backend

* Python
* Flask (web framework)

### Database

* SQLite (development)
* PostgreSQL (optional, for deployment)
* SQLAlchemy (ORM for all backend reads, writes & business logic)

### Frontend

* HTML / CSS / JavaScript
* Jinja2 (Flask's server-side templating)

### Auth

* Flask-Login (session management)
* Werkzeug (password hashing)

### External API

* Google Books API (auto-populates title, author, genre, and cover image when a book is added)

### Deployment

* Render (free tier; chosen over Heroku/Firebase/Netlify/Vercel since this is a Python/Flask app with a relational database, not a static site or Google-backend service)

## Architecture

Flask routes handle all reads, writes, and business logic through SQLAlchemy. Four related tables — `Users`, `Books`, `Reviews`, `Discussions` — are linked by foreign keys, with `Discussions` using a self-referencing foreign key (`parent_id`) to support nested replies. The backend recursively reconstructs that flat comment data into a nested tree before Jinja2 renders it as HTML.

## Setup

**Prerequisites:** Python 3.11+, pip, and Git.

```
git clone https://github.com/Aolkiji/ChapterChat.git
cd ChapterChat
```

### Backend (Flask)

```
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run                     # starts the dev server at localhost:5000
```

**Not set up yet** (these steps will be added here as they land):

* Environment variables: `.env` will need a `SECRET_KEY`, `DATABASE_URL`, and a `GOOGLE_BOOKS_API_KEY`. `.env` files are gitignored; never commit them.
* Database: run the initial migration to create the `Users`, `Books`, `Reviews`, and `Discussions` tables.
* Wiring: route blueprints (`auth_routes.py`, `book_routes.py`, `review_routes.py`, `discussion_routes.py`) are still being built out and are not all registered in `app.py` yet.


## Status

Early build — database schema and core CRUD for Books are in progress, user authentication is being scaffolded next. Frontend is HTML/CSS/JS served through Jinja2 templates; no styling pass yet.

## Contributors

* Emmanuel Athias
