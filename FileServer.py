from flask import Flask, request, jsonify, redirect, url_for, flash
import os, uuid, sys
from werkzeug.utils import secure_filename
from flask import send_from_directory
import requests
import config
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def list_files(startpath):
    result = ""
    edit_times = {}
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        result = addLine(result,'{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            result = addLine(result,'{}{}'.format(subindent, f))
    return result

def addLine(fullStr, lineToAdd):
    return (fullStr + "\n" + lineToAdd)

@app.route("/get_last_edit_time", methods=["GET"])
def get_last_edit_time():
    data = request.form
    filename = data["filename"]
    time = os.path.getmtime(UPLOAD_FOLDER+"/"+filename)
    return str(time)

@app.route('/get_directory_list', methods=['GET'])
def updateDirService():
    dirs = list_files(UPLOAD_FOLDER)
    return dirs;

def updateDirectoryService():
    dirs = list_files(UPLOAD_FOLDER)
    print(type(dirs))
    msg = {"key": dirs}
    print(msg)
    print("Sending update to directory service!")
    msg = requests.post("http://localhost:9001/update_directories", data = msg)
    print(msg.text)
    return("Done")

@app.route('/delete', methods=["POST"])
def delete_file():
    try:
        os.remove(UPLOAD_FOLDER+"/"+request.form["key"])
        return "Successfully deleted file"
    except FileNotFoundError:
        print("Error - No such file : " + request.form["key"])
        return "Error, no such file."

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("Trying to get filename: " + filename)
    try:
        return send_from_directory(UPLOAD_FOLDER,filename)
    except FileNotFoundError:
        return "Error: File not found on servers."
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "No file attached to request"
        myfile = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if myfile.filename == '':
            return "No file name"
        if myfile and allowed_file(myfile.filename):
            filename = secure_filename(myfile.filename)
            current_path = os.getcwd()
            save_location= current_path + "/" + (app.config["UPLOAD_FOLDER"] + "-" + sys.argv[1]) + "/" + filename
            print("Saving " + filename + " to " + save_location)
            myfile.save(save_location)
        else:
            print("Error somewhere")

    return "GET I think but I'm not sure"


if __name__ == '__main__':
    try:
        os.mkdir((app.config["UPLOAD_FOLDER"] + "-" + sys.argv[1]))
    except:
        print("Upload Dir exists")
    app.run(debug=True,host="localhost", port=int(sys.argv[1]))
