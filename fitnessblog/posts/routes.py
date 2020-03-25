from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from fitnessblog import db
from fitnessblog.models import Post
from fitnessblog.posts.forms import PostForm

posts = Blueprint("posts", __name__)

# Create a new post
@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Construct new post and save to db
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


# Get a specific post by id
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


# Update a post
@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if user owns post before updating
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # Validate form data, update db, redirect to post page
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    # If get request, populate form with the current values from db
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        post.category = post.category
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


# Delete a post
@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if user owns post before updating
    if post.author != current_user:
        abort(403)
    # Remove post from db, flash message, redirect to home
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))


# Filter posts by category
@posts.route("/category/<string:category>", methods=["GET"])
@login_required
def filter_by_category(category):
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter_by(category=category).paginate(page=page, per_page=5)
    return render_template("category_list.html", posts=posts)


# Filter posts by latest
@posts.route("/latest", methods=["GET"])
@login_required
def latest_posts():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter_by(category=category).paginate(page=page, per_page=5)
    return render_template("latest_posts.html", posts=posts)
