from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models import db, User

auth = Blueprint("auth", __name__)

# REGISTER: show the form (GET) and create a new user (POST)

auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm", "").strip()

        errors = []
        if not username or not email or not password:
            errors.append("All fields are required.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if User.query.filter_by(username=username).first():
            errors.append("Username is already taken.")
        if User.query.filter_by(email=email).first():
            errors.append("Email is already registered.")

        if errors:
            for error in errors:
                flash(error, "error")
                # Re-show the form with what they already typed but not the password
            return render_template("register.html", username=username, email=email)

        user =User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Registration successful. You are now logged in.", "success")
        return redirect(url_for("main.index"))
    return render_template("register.html")


#Login: show the form (GET) and log in the user (POST)
@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()

        if user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return render_template("login.html", email=email)

        login_user(user, remember=remember)
        flash("Logged in successfully.", "success")


        next_page = request.args.get("next")
        if next_page or next_page.startswith("/"):
            redirect(next_page)
        return redirect(url_for("main.index"))

    return render_template("login.html")

# Logout: log out the user (GET)
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))




