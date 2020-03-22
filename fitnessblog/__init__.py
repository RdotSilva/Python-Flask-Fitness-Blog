from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from fitnessblog.config import Config


# Create DB instance
db = SQLAlchemy()

# Bcrypt PW hashing
bcrypt = Bcrypt()

# Flask Login
login_manager = LoginManager()

# Set initial login view & message
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    # Use config values from config file
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import routes from Blueprints
    from fitnessblog.users.routes import users
    from fitnessblog.posts.routes import posts
    from fitnessblog.main.routes import main
    from fitnessblog.errors.handlers import errors

    # Register routes from Blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
