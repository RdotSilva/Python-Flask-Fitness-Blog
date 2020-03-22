from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

# Handle 404 errors
@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404


# Handle 403 errors
@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/403.html"), 403
