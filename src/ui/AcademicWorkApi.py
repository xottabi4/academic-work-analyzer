import json
import os

from flask import request, Flask, render_template, flash, redirect, url_for, get_flashed_messages
from werkzeug.exceptions import HTTPException

from definitions import resourcesStoragePath
from src.ui.AcademicWorkProcessor import processAcademicWorkFile, extractDataFromAbstract

ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = os.path.join(resourcesStoragePath, "downloads")
app = Flask(__name__, template_folder=os.path.join(resourcesStoragePath, "templates"))
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'Dnb!R#3i%z#090l4'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    errorMessage = get_flashed_messages()
    if not errorMessage:
        errorMessage = None
    else:
        errorMessage = errorMessage[0]
    # errorMessage = None
    jsonData = None
    fileName = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            errorMessage = "No file part"
        else:
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            fileName = file.filename
            if file.filename == '':
                errorMessage = "No selected file"
            else:
                if not allowed_file(file.filename):
                    errorMessage = "Selected file is not PDF"
                else:
                    # filename = secure_filename(file.filename)
                    # pathToFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    # file.save(pathToFile)
                    processedData = processAcademicWorkFile(file)
                    jsonData = json.dumps(processedData, ensure_ascii=False, sort_keys=False, indent=2)
    return render_template("new_file_upload_form.html", errorMessage=errorMessage, response=jsonData, fileName=fileName)


@app.route('/upload/text', methods=['POST'])
def upload_text():
    receivedText = request.form["text"]
    if not receivedText:
        return "RECEIVED EMPTY REQUEST!!!"
    else:
        processedData = extractDataFromAbstract(receivedText)
        return json.dumps(processedData, ensure_ascii=False, sort_keys=False, indent=2)


@app.errorhandler(HTTPException)
def all_exception_handler(error):
    if error:
        errorMesage = "You got error {}!".format(error.code)
    else:
        errorMesage = None
    return render_template("error_page.html", error=errorMesage, homePage=url_for('upload_file'))


@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File too large')
    return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(debug=True)
