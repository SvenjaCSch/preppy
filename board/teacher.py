from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

bp = Blueprint("teacher", __name__)

@bp.route('/teacher_landing')
@login_required
def landing():
    if current_user.role != 'teacher':
        return redirect(url_for('auth.login'))
    return render_template("teacher/landing.html", name=current_user.name)

@bp.route('/upload')
@login_required
def upload():
    return render_template('teacher/upload.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        upload_path = os.path.join(current_app.instance_path, 'pdfs', secure_filename(f.filename))
        f.save(upload_path)
        return render_template('teacher/upload.html')
