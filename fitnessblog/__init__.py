from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

# Temporary secret key, will change this and make env variable later
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

# Create DB instance
db = SQLAlchemy(app)
