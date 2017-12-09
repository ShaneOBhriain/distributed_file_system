import sys
import requests



def printOptions():
    instructions = "Choose an option from the following by typing the corresponding number and the arguments after it.\nFor example, to upload 'foo.png' you would type '2 foo.png'\n"
    options = "--------------------\n1. Specify local directory for files you are uploading.\n2. Upload file.\n3. Download file.\n4. List directories.\n--------------------\n"
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

# def downloader():

def listDirectories():
    print("Asking for list of dirs")
    msg = requests.get("http://localhost:3473/get_directories")
    print("msg")
    print(msg.text)

def main():
    printOptions()
    cmd = input("Enter your command: ")
    print(cmd.split())
    cmdList = cmd.split()
    if cmdList[0]!="ls" and len(cmdList) !=2:
        print("Incorrect number of arguments")
    if cmdList[0] == "upload":
        uploader(cmdList[1])
    if cmdList[0] == "download":
        downloader(cmdList[1])
    if cmdList[0] == "ls":
        listDirectories()
    main()
main()
