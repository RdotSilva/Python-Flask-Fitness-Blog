from flask import render_template, request, Blueprint
from fitnessblog.models import Post

main = Blueprint("main", __name__)

# Handle multiple routes using the same function
@main.route("/")
@main.route("/home")
# url_for refers to the function name below (home)
def home():
    # Get page argument (start at default page 1)
    page = request.args.get("page", 1, type=int)
    # Fetch all posts from db sorting by date desc, using pagination
    # Page is taken from arg above, per_page is number of results per page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
