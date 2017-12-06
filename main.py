from flask import Flask, request, jsonify, redirect, url_for, flash
import os, uuid
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No file attached to request"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "No file name"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("filename")
            print(filename)
            print(os.getcwd())
            current_path = os.getcwd()
            save_location= current_path + "/" + app.config["UPLOAD_FOLDER"] + filename
            print("Saving " + filename + " to " + save_location)
            file.save(save_location)
    return "GET I think but I'm not sure"


if __name__ == '__main__':
    app.run(debug=True,host="localhost", port=2586)
