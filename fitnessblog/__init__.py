from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, MAIL_USER, MAIL_PASS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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

# Mail config settings
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = MAIL_USER
app.config["MAIL_PASSWORD"] = MAIL_PASS
mail = Mail(app)

# Import routes from Blueprints
from fitnessblog.users.routes import users
from fitnessblog.posts.routes import posts
from fitnessblog.main.routes import main

# Register routes from Blueprints
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
