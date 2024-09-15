import os
from flask import Flask, request, jsonify, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'documents'
app.config['SECRET_KEY'] = 'supersecretkey'

if not os.path.exists('api/documents'):
    os.makedirs('api/documents')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    form = UploadFileForm()
    
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],file.filename))

        return render_template('successful_upload.html')
    
    return render_template('index.html', form=form)


@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        return jsonify({'message': 'File successfully uploaded', 'filename': file.filename, 'filepath': filepath}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400


@app.route('/health', methods=["GET"])
def health_check():
    return jsonify({'status': 'API is running'}), 200


if __name__ == '__main__':
    app.run(debug=True)
