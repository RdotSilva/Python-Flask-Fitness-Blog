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
