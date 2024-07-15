from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint("pages", __name__)

@bp.route("/")
def home():
    return render_template("pages/home.html")

@bp.route("/about")
def about():
    return render_template("pages/about.html")

@bp.route('/profile')
@login_required
def profile():
    return render_template('pages/profile.html', name=current_user.name)


