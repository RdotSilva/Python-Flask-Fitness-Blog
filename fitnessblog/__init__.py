from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Config variables imported from config.py
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

# Create DB instance
db = SQLAlchemy(app)

# Bcrypt PW hashing
bcrypt = Bcrypt(app)

# Flask Login
login_manager = LoginManager(app)

# Set initial login view & message
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from fitnessblog import routes
