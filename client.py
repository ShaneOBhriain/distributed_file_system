import sys
import requests
import time
import config
import os

last_download_time = {}

def printOptions():
    instructions = "\n\nChoose an option'\n"
    options = "--------------------\n1. Specify local directory for files you are uploading.\n2. Upload file. (upload 'filename')\n3. Download file. (download 'filename')\n4. Delete File (del 'filename') \n5. List directories. (ls)\n--------------------\n"
    print(instructions + options)

def uploader(filename):
    try:
        with open(filename,'rb') as fileToSend:
            files = {'file':fileToSend}
            msg = requests.post("http://localhost:9001/replicate",files=files)
            if msg.status_code == 200:
                print("Successfully uploaded file")
            else:
                print("Error on upload server.")
    except FileNotFoundError:
        print("Error: " + filename + " not found.")

def downloader(filename):
    print("Checking last edit time")

    should_download = True

    req = {"filename": filename}
    last_edit_time = requests.get("http://localhost:9001/get_last_edit_time", data=req)
    result_file = config.DOWNLOAD_FOLDER+"/"+filename
    if filename in os.listdir(config.DOWNLOAD_FOLDER):
        local_last_edit = os.path.getmtime(result_file)
        if(local_last_edit > float(last_edit_time.text)):
            print("Using cached file")
            should_download = False
    if should_download:
        url = "http://localhost:8001/uploads/" + filename
        res = requests.get(url)
        last_download_time[filename] = time.time()
        with open(result_file,'wb') as fileToWrite:
            fileToWrite.write(res.content)
        print("Downloaded and wrote to file: " + result_file)

def deleteFile(filename):
    msg = {"key": filename}
    res = requests.post("http://localhost:8001/delete", data = msg)
    print(res.text)


def listDirectories():
    print("Asking for list of dirs")
    msg = requests.get("http://localhost:9001/get_directories")
    print("msg")
    print(msg.text)

def main():
    printOptions()
    cmd = input("Enter your command: ")
    cmdList = cmd.split()
    if cmdList[0]!="ls" and len(cmdList) !=2:
        print("Incorrect number of arguments")
    if cmdList[0] == "upload":
        uploader(cmdList[1])
    elif cmdList[0] == "download":
        downloader(cmdList[1])
    elif cmdList[0] == "ls":
        listDirectories()
    elif cmdList[0] == "del":
        deleteFile(cmdList[1])
    main()
main()
