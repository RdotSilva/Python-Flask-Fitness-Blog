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

