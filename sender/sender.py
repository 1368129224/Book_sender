import os
from flask import Flask, flash, request, redirect, url_for
from flask import (
    Blueprint, flash, redirect, render_template, request
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from . import UPLOAD_FOLDER
from .utils import send_email


bp = Blueprint('sender', __name__)
ALLOWED_EXTENSIONS = {'txt', 'mobi', 'doc', 'docx', 'rtf', 'pdf'}

@bp.route('/')
def index():
    return render_template('sender/index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=('POST', 'GET'))
def upload():
    if 'file' not in request.files:
        print(request.files)
        flash('No file part')
        return '-1'
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return '-2'
    if file and allowed_file(file.filename):
        print(request.form)
        email = request.form.to_dict().get('email')
        print(email)
        filename = secure_filename(file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        send_email(email, UPLOAD_FOLDER, filename)
        return '0'
