from fitnessblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config_secret import SECRET
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# DB models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_type = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    # This line sets the relationship to the post model (one to many), backref allows us to get author of post
    posts = db.relationship("Post", backref="author", lazy=True)

    # Create a reset token using secret
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(SECRET, expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    # Verify the reset token and return user if good
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(SECRET)
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    # Used to indicate how the user will look when printed
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    # Set foreign key relationship for user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Used to indicate how the post will look when printed
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
