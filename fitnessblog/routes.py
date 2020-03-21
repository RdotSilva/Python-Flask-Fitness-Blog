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

