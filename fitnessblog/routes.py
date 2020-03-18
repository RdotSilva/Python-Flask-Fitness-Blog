import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from fitnessblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from fitnessblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
        return redirect(url_for("login"))

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
            # Check for any next parameter arguments
            next_page = request.args.get("next")
            # Ternary to send user to next page if it exists, otherwise send user to home page
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Check email or password", "danger")

    return render_template("login.html", title="Login", form=form)


# Log user out and redirect to home page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


# Save user profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # Split filename to get the file extension. Using _ as variable for f_name because it will be unused
    _, f_ext = os.path.splitext(form_picture.filename)
    # Create new picture file name using hex and file extension
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_filename)

    # Resize picture
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)

    # Save profile picture to path above
    image.save(picture_path)
    return picture_filename


# User account page
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    # Check if form data is valid, update user account info in database, redirect to account page
    if form.validate_on_submit():
        # Check for picture data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    # Set profile picture image file
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


# Create a new post
@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form)

