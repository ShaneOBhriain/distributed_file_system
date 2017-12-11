import sys
import requests



def printOptions():
    instructions = "Choose an option from the following by typing the corresponding number and the arguments after it.\nFor example, to upload 'foo.png' you would type '2 foo.png'\n"
    options = "--------------------\n1. Specify local directory for files you are uploading.\n2. Upload file.\n3. Download file.\n4. Delete File \n5.List directories.\n--------------------\n"
    print(instructions + options)

def uploader(filename):
    try:
        with open(filename,'rb') as fileToSend:
            files = {'file':fileToSend}
            msg = requests.post("http://localhost:2586/upload",files=files)
            if msg.status_code == 200:
                print("Successfully uploaded file")
            else:
                print("Error on upload server.")
    except FileNotFoundError:
        print("Error: " + filename + " not found.")

def downloader(filename):
    url = "http://localhost:2586/uploads/" + filename
    res = requests.get(url)
    with open(filename,'wb') as fileToWrite:
        fileToWrite.write(res.content)
    print("Downloaded and wrote to file: " + filename)

def deleteFile(filename):
    msg = {"key": filename}
    res = requests.post("http://localhost:2586/delete", data = msg)
    print(res.text)


def listDirectories():
    print("Asking for list of dirs")
    msg = requests.get("http://localhost:3473/get_directories")
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
