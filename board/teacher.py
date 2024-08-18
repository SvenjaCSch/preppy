from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import PyPDF2

bp = Blueprint("teacher", __name__)

@bp.route('/teacher_landing')
@login_required
def landing()->str:
    """
    passes to landing page if teacher otherwise login page
    """
    if current_user.role != 'teacher':
        return redirect(url_for('auth.login'))
    return render_template("teacher/landing.html", name=current_user.name)

@bp.route('/upload')
@login_required
def upload()->str:
    """
    passes to upload page
    """
    return render_template('teacher/upload.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file()->str:
    """
    uploads pdf and turns it into text
    """
    if request.method == 'POST':
        f = request.files['file']
        pdf_folder = os.path.join(current_app.instance_path, 'pdfs')
        text_folder = os.path.join(current_app.instance_path, 'texts')

        # Create directories if they don't exist
        os.makedirs(pdf_folder, exist_ok=True)
        os.makedirs(text_folder, exist_ok=True)

        upload_path = os.path.join(pdf_folder, secure_filename(f.filename))
        f.save(upload_path)
        
        # Open the saved file for reading
        with open(upload_path, 'rb') as file:
            pdfreader = PyPDF2.PdfFileReader(file)
            num_pages = pdfreader.numPages
            
            # Iterate through all pages and extract text
            text = ""
            for page_num in range(num_pages):
                pageobj = pdfreader.getPage(page_num)
                text += pageobj.extractText()  
            
            # Write the extracted text to a file
            text_path = os.path.join(text_folder, 'text.txt')
            with open(text_path, 'a', encoding='utf-8') as file1:
                file1.write(text)
        
        return render_template('teacher/upload.html')