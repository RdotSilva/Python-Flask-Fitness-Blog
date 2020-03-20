import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from fitnessblog.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    PostForm,
    RequestResetForm,
    ResetPasswordForm,
)
from fitnessblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# These imports come from __init__.py - You can use the full package name instead of __init__.py (fitnessblog)
from fitnessblog import app, db, bcrypt, mail
from flask_mail import Message

# Handle multiple routes using the same function
@app.route("/")
@app.route("/home")
# url_for refers to the function name below (home)
def home():
    # Get page argument (start at default page 1)
    page = request.args.get("page", 1, type=int)
    # Fetch all posts from db sorting by date desc, using pagination
    # Page is taken from arg above, per_page is number of results per page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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
        # Construct new post and save to db
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


# Get a specific post by id
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


# Update a post
@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if user owns post before updating
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # Validate form data, update db, redirect to post page
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    # If get request, populate form with the current values from db
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


# Delete a post
@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if user owns post before updating
    if post.author != current_user:
        abort(403)
    # Remove post from db, flash message, redirect to home
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))


# Show all posts by specific user
@app.route("/user/<string:username>")
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


# Send user reset password email with token
def send_reset_email(user):
    # Get token
    token = user.get_reset_token()
    # Send user email message with token
    msg = Message(
        "Password Reset Request",
        sender="noreply@rdotsilva.com",
        recipients=[user.email],
    )
    # Compose the email body
    msg.body = f"To reset your email please visit the following link: {url_for('reset_token', token=token, _external=True)} If you did not make this request please ignore this email."
    # Send the message
    mail.send(msg)


# Create a request for password reset
@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    # If valid form is submitted get the user based off of email, and send that user an email with token
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


# Reset password using token
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    # Call the verify_reset_token method from User model, return user if token is valid
    user = User.verify_reset_token(token)
    # Token invalid
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
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
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)

