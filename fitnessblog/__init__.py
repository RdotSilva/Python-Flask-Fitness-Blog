from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from fitnessblog.config import Config

app = Flask(__name__)

# Use config values from config file
app.config.from_object(Config)


# Create DB instance
db = SQLAlchemy(app)

# Bcrypt PW hashing
bcrypt = Bcrypt(app)

# Flask Login
login_manager = LoginManager(app)

# Set initial login view & message
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


mail = Mail(app)

# Import routes from Blueprints
from fitnessblog.users.routes import users
from fitnessblog.posts.routes import posts
from fitnessblog.main.routes import main

# Register routes from Blueprints
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
