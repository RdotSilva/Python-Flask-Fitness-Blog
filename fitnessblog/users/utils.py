import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from fitnessblog import app, mail

# Save user profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # Split filename to get the file extension. Using _ as variable for f_name because it will be unused
    _, f_ext = os.path.splitext(form_picture.filename)
    # Create new picture file name using hex and file extension
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_filename)

    # Resize picture
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)

    # Save profile picture to path above
    image.save(picture_path)
    return picture_filename


# Send user reset password email with token
def send_reset_email(user):
    # Get token
    token = user.get_reset_token()
    # Send user email message with token
    msg = Message(
        "Password Reset Request",
        sender="noreply@rdotsilva.com",
        recipients=[user.email],
    )
    # Compose the email body
    msg.body = f"To reset your email please visit the following link: {url_for('users.reset_token', token=token, _external=True)} If you did not make this request please ignore this email."
    # Send the message
    mail.send(msg)
