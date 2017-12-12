import os
import config
import time

directory = ""

from flask import Flask, request, jsonify, redirect, url_for, flash
import os, uuid
from werkzeug.utils import secure_filename
from flask import send_from_directory
import requests
app = Flask(__name__)

directories = ""

last_edit_time = {}

def initialize_server_info():
    for server_port in config.file_server_ports:
        last_edit_time[server_port] = []
    print("Initialized server info.")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def updateDirectoryList():
    global directories
    res = requests.get("http://localhost:" + str(config.file_server_ports[0])+"/get_directory_list")
    directories = res.text

@app.route("/get_last_edit_time", methods=["GET"])
def get_last_edit_time():
    data = request.form
    filename = data["filename"]
    msg = {"filename": filename}
    req = requests.get("http://localhost:" + str(config.file_server_ports[0]) + "/get_last_edit_time",data=msg)
    print("LAST EDIT TIME: " + req.text)
    return req.text

@app.route("/replicate", methods=["POST"])
def replicate():
    myfile = request.files['file']
    filename = myfile.filename
    last_edit_time[filename] = time.time()
    current_path = os.getcwd()
    save_location= current_path + "/tmp/" + filename
    myfile.save(save_location)
    with open(save_location,'rb') as fileToSend:
        files = {'file':fileToSend}
        for server_port in config.file_server_ports:
            server_url = "http://localhost:" + str(server_port) + "/upload"
            msg = requests.post(server_url,files=files)
    if msg.status_code == 200:
        print("Successfully replicated file")
    else:
        print("Error replicating.")

    updateDirectoryList()
    return "Replicated"

@app.route("/delete",methods=["POST"])
def distributeDeletes():
    filename = request.form["filename"]
    print("Deleting " + filename + " from all servers")
    msg = {"filename": filename}
    for server_port in config.file_server_ports:
        server_url = "http://localhost:" + str(server_port) + "/delete"
        msg = requests.post(server_url,data=msg)
    return "Done"
@app.route('/get_directories', methods=['GET'])
def getDirectoryList():
    updateDirectoryList()
    return directories

if __name__ == '__main__':
    try:
        os.mkdir("tmp")
    except:
        print("tmp folder exists.")
    initialize_server_info()
    updateDirectoryList()
    app.run(debug=True,host="localhost", port=config.directory_service_port)
