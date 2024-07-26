from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint("teacher", __name__)

@bp.route('/teacher_landing')
@login_required
def landing():
    if current_user.role != 'teacher':
        return redirect(url_for('auth.login'))
    return render_template("teacher/landing.html", name=current_user.name)