from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint("student", __name__)

@bp.route("/landing")
@login_required
def landing():
    return render_template("student/landing.html", name=current_user.name)

@bp.route('/chatbot')
@login_required
def profile():
    return render_template('student/chatbot.html', name=current_user.name)