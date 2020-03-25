from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from fitnessblog import db, bcrypt
from fitnessblog.models import User, Post
from fitnessblog.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from fitnessblog.users.utils import save_picture, send_reset_email

# Create blueprint instance
users = Blueprint("users", __name__)

# Registration route using the register form in forms.py
@users.route("/register", methods=["GET", "POST"])
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
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            profile_type=form.profile_type.data,
        )
        # Save user to db
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created. Please log in", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


# Login route using the login form in forms.py
@users.route("/login", methods=["GET", "POST"])
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
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful. Check email or password", "danger")

    return render_template("login.html", title="Login", form=form)


# Log user out and redirect to home page
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


# User account page
@users.route("/account", methods=["GET", "POST"])
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
        current_user.profile_type = form.profile_type.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.profile_type.data = current_user.profile_type
    # Set profile picture image file
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


# Show all posts by specific user
@users.route("/user/<string:username>")
# url_for refers to the function name below (home)
def user_posts(username):
    # Get page argument (start at default page 1)
    page = request.args.get("page", 1, type=int)
    # Get first user with this username or return 404
    user = User.query.filter_by(username=username).first_or_404()
    # Fetch all posts from db sorting by date desc, filter by specific user, using pagination
    # Page is taken from arg above, per_page is number of results per page
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_posts.html", posts=posts, user=user)


# Create a request for password reset
@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    # If valid form is submitted get the user based off of email, and send that user an email with token
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


# Reset password using token
@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    # Call the verify_reset_token method from User model, return user if token is valid
    user = User.verify_reset_token(token)
    # Token invalid
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    # Token Valid send user to reset password form
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        # Update user password in db
        user.password = hashed_password
        db.session.commit()
        flash("Password has been updated! Please log in", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
