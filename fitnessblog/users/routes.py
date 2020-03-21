from flask import Blueprint

# Create blueprint instance
users = Blueprint("users", __name__)

# Registration route using the register form in forms.py
@app.route("/register", methods=["GET", "POST"])
def register():
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect("home")
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        # Construct new user
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        # Save user to db
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created. Please log in", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


# Login route using the login form in forms.py
@app.route("/login", methods=["GET", "POST"])
def login():
    # If user already signed in redirect to home page
    if current_user.is_authenticated:
        return redirect("home")
    form = LoginForm()
    if form.validate_on_submit():
        # Get user in db by email
        user = User.query.filter_by(email=form.email.data).first()
        # Check users hashed password matches typed password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # Check for any next parameter arguments
            next_page = request.args.get("next")
            # Ternary to send user to next page if it exists, otherwise send user to home page
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Check email or password", "danger")

    return render_template("login.html", title="Login", form=form)


# Log user out and redirect to home page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
