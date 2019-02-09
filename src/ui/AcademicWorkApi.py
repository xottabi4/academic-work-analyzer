import json
import os

from flask import request, Flask, render_template

from definitions import resourcesStoragePath
from ui.AcademicWorkProcessor import processAcademicWorkFile

ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = os.path.join(resourcesStoragePath, "downloads")
app = Flask(__name__, template_folder=os.path.join(resourcesStoragePath, "templates"))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    errorMessage = None
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
                    jsonData = json.dumps(processedData, ensure_ascii=False)
    return render_template("file_upload_form.html", errorMessage=errorMessage, response=jsonData, fileName=fileName)


# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#         filename)


@app.errorhandler(Exception)
def all_exception_handler(error):
    return "404 Not Found", 404
    # return error


if __name__ == '__main__':
    app.run(debug=True)
