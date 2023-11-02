from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

#404 error to prevent pages browsering
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

#error for 403 to prevent users from accessing file not theirs
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

#500 error for page not loading (server error)
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
