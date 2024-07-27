from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import PyPDF2

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
        
        # Open the saved file for reading
        with open(upload_path, 'rb') as file:
            pdfreader = PyPDF2.PdfFileReader(file)
            num_pages = pdfreader.numPages
            
            # Iterate through all pages and extract text
            text = ""
            for page_num in range(num_pages):
                pageobj = pdfreader.getPage(page_num)
                text += pageobj.extract_text()  # Note: use extract_text() instead of extractText() for PyPDF2 v2.x+
            
            # Write the extracted text to a file
            text_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')
            with open(text_path, 'a', encoding='utf-8') as file1:
                file1.write(text)
        
        return render_template('teacher/upload.html')
