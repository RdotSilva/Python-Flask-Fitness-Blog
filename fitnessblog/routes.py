from flask import render_template, url_for, flash, redirect
from fitnessblog.forms import RegistrationForm, LoginForm
from fitnessblog.models import User, Post
from flask_login import login_user, current_user, logout_user

# These imports come from __init__.py - You can use the full package name instead of __init__.py (fitnessblog)
from fitnessblog import app, db, bcrypt

posts = [
    {
        "author": "Ryan Silva",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2020",
    },
    {
        "author": "Mike Silva",
        "title": "Blog Post 2",
        "content": "2nd post content",
        "date_posted": "May 2, 2020",
    },
]

# Handle multiple routes using the same function
@app.route("/")
@app.route("/home")
# url_for refers to the function name below (home)
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


# Registration route using the register form in forms.py
@app.route("/register", methods=["GET", "POST"])
def register():
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect("home")
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        # Construct new user
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        # Save user to db
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created. Please log in", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)


# Login route using the login form in forms.py
@app.route("/login", methods=["GET", "POST"])
def login():
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect("home")
    form = LoginForm()
    if form.validate_on_submit():
        # Get user in db by email
        user = User.query.filter_by(email=form.email.data).first()
        # Check users hashed password matches typed password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Send user to home page if login success
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Check email or password", "danger")

    return render_template("login.html", title="Login", form=form)


# Log user out and redirect to home page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


# User account page
@app.route("/account")
def account():
    return render_template("account.html", title="Account")
