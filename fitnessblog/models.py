from flaskblog import db
from datetime import datetime

# DB models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    # This line sets the relationship to the post model (one to many), backref allows us to get author of post
    posts = db.relationship("Post", backref="author", lazy=True)

    # Used to indicate how the user will look when printed
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # Set foreign key relationship for user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Used to indicate how the post will look when printed
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
