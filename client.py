import sys
import requests
import time
import config
import os

last_download_time = {}

def printOptions():
    instructions = "\n\nChoose an option'\n"
    options = "--------------------\n1. Specify download folder. (set_download_folder 'filename')\n2. Upload file. (upload 'filename')\n3. Download file. (download 'filename')\n4. Delete File (del 'filename') \n5. List directories. (ls)\n6. Lock Operations on File (lock/unlock/locked 'filename')\n--------------------\n"
    help_cmd = "\n\nTo see this menu again, simply use the 'help' command\n"
    print(instructions + options + help_cmd)

def lock_file(filename):
    msg = {"filename":filename}
    res = requests.post(config.lock_service_url+"/lock",data=msg)
    if res.status_code == 200:
        print(res.text)

def unlockFile(filename):
    msg = {"filename":filename}
    res = requests.post(config.lock_service_url+"/unlock",data=msg)
    if "Error" not in res.text:
        print("Successfully unlocked " + filename)
    else:
        print(res.text)

def getLockStatus(filename):
    req={"filename":filename}
    msg = requests.get(config.lock_service_url+"/lock_status",data=req)
    if(bool(int(msg.text))):
        print(filename + " Lock Status: Locked.")
        return True
    else:
        print(filename + " Lock Status: Not Locked.")
        return False

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
    if(getLockStatus(filename)):
        print("Error: File is locked and can not be downloaded.")
        return False
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
        if("404" in res.text):
            print("Error: File not found on server.")
        else:
            with open(result_file,'wb') as fileToWrite:
                fileToWrite.write(res.content)
            print("Downloaded and wrote to file: " + result_file)

def deleteFile(filename):
    msg = {"filename": filename}
    res = requests.post(config.directory_service_url+"/delete", data = msg)
    print(res.text)

def listDirectories():
    msg = requests.get("http://localhost:9001/get_directories")
    print(msg.text)

def setDownloadDir(dir_name):
    try:
        os.mkdir(dir_name)
        config.DOWNLOAD_FOLDER = dir_name
    except:
        config.DOWNLOAD_FOLDER = dir_name

def main(first_run):
    if(first_run):
        printOptions()
        setDownloadDir(config.DOWNLOAD_FOLDER)
    cmd = input(">: ")
    cmdList = cmd.split()
    if(cmdList[0]=="help"):
        printOptions()
    elif cmdList[0] == "ls":
        listDirectories()
    elif len(cmdList) <2:
        print("Invalid input")
    elif cmdList[0] == "upload":
        uploader(cmdList[1])
    elif cmdList[0] == "download":
        downloader(cmdList[1])
    elif cmdList[0] == "ls_available_uploads":
        listAvailableUploads()
    elif cmdList[0] == "del":
        deleteFile(cmdList[1])
    elif cmdList[0] == "lock":
        lock_file(cmdList[1])
    elif cmdList[0] == "locked":
        getLockStatus(cmdList[1])
    elif cmdList[0] == "unlock":
        unlockFile(cmdList[1])
    elif cmdList[0] == "set_download_folder":
        setDownloadDir(cmdList[1])
    else:
        print("Invalid input.")
    main(False)
main(True)
