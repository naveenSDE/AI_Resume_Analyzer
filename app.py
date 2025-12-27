import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.parser import extract_text_from_pdf, extract_text_from_docx
from utils.nlp import analyze_resume

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

ALLOWED_EXTENSIONS = {'pdf', 'docx'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resume']
        job_description = request.form.get('job_description')

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                resume_text = extract_text_from_pdf(filepath)
            elif filename.lower().endswith('.docx'):
                resume_text = extract_text_from_docx(filepath)
            else:
                flash('Unsupported file format')
                return redirect(request.url)

            # Analyze resume
            analysis_results = analyze_resume(resume_text, job_description)

            # Clean up uploaded file
            os.remove(filepath)

            return render_template('result.html', results=analysis_results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
