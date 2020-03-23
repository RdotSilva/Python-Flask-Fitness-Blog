from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("cardio", "Cardio"),
            ("weight", "Weight Training"),
            ("diet", "Diet"),
            ("other", "Other"),
        ],
    )
    submit = SubmitField("Post")
