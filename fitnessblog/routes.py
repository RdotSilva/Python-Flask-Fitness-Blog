from models import User, Post

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
# url_for refers to the function name below (home)
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


# Registration route using the register form in forms.py
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)


# Login route using the login form in forms.py
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Temporary dummy validation
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Check username or password", "danger")

    return render_template("login.html", title="Login", form=form)