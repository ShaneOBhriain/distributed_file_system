import os

directory = ""

from flask import Flask, request, jsonify, redirect, url_for, flash
import os, uuid
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)

directories = ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/update_directories', methods =["POST"])
def update_directories():
    global directories
    filenames = request.form
    directories = filenames["key"]
    return "Successfully updated directories"

@app.route('/get_directories', methods=['GET'])
def getDirectoryList():
    print("He wants to get the directory list")
    print(directories)
    return directories


if __name__ == '__main__':
    app.run(debug=True,host="localhost", port=3473)
