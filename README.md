ChapterChat

A web application for online book clubs: track what you're reading, rate and review books, and hold threaded discussions with your club members on your own schedule, without needing everyone online at the same time.

The Problem

Online book clubs currently have no dedicated platform to call home. Groups that want to read and discuss books together are forced into being online at the same time, relying on live chats or scheduled calls just to talk about what they've read. This doesn't work for people with different schedules, time zones, or reading paces, forcing them to miss the conversation entirely.

ChapterChat solves this by combining structured book data (ratings, reviews) with asynchronous, threaded discussion — so members can catch up and contribute whenever they have time.

Features
 Books : Add, edit, and delete books (title, author, genre, cover image), auto-populated via the Google Books API
 Reviews & Ratings : Users rate books (1–5 stars) and write reviews
 Discussions : Threaded, nested comment discussions per book
 Users : Register, log in, and manage a profile
Tech Stack
 Backend: Flask
 Database:	SQLite 
 ORM:	SQLAlchemy
 Templating:	Jinja2
 Frontend: 	HTML, CSS, JavaScript
 Authentication: Flask-Login
 External API:	Google Books API
 
