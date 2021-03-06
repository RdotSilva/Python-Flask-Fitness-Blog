from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    InputRequired,
)
from flask_login import current_user
from fitnessblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "ConfirmPassword", validators=[DataRequired(), EqualTo("password")]
    )
    profile_type = RadioField(
        "Profile Type",
        choices=[("instructor", "Instructor"), ("student", "Student"),],
        validators=[InputRequired()],
    )
    submit = SubmitField("Sign Up")

    # Check if username exists in db
    def validate_username(self, username):
        # Check for user and get first one there, if not return none
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken. Choose another username.")

    # Check if email exists in db
    def validate_email(self, email):
        # Check for email and get first one there, if not return none
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                "Email address already registered. Choose another email."
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    profile_type = RadioField(
        "Profile Type", choices=[("instructor", "Instructor"), ("student", "Student"),]
    )
    submit = SubmitField("Update")
    # TODO: Add image update

    # Check if username exists in db
    def validate_username(self, username):
        if username.data != current_user.username:
            # Check for user and get first one there, if not return none
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is taken. Choose another username.")

    # Check if email exists in db
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Request Password Reset")

    # Check if email exists in db
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError("There is no account using that email address.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "ConfirmPassword", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
