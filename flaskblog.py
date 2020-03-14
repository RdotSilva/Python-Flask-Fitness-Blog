from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Temporary secret key, will change this and make env variable later
app.config["SECRET_KEY"] = "b745125d03ae68e8a939473072208d98"

posts = [
    {
        "author": "Ryan Silva",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20, 2020",
    },
    {
        "author": "Mike Silva",
        "title": "Blog Post 2",
        "content": "2nd post content",
        "date_posted": "May 2, 2020",
    },
]

# Handle multiple routes using the same function
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


# Registration route using the register form in forms.py
@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Register", form=form)


# Run in debug mode, avoiding the use of ENV variable with the flask run command
if __name__ == "__main__":
    app.run(debug=True)
