from flask import Flask, request
import config

app = Flask(__name__)

locked_files = []

@app.route('/lock', methods=['POST'])
def lock():
    filename = request.form["filename"]
    try:
        file_index = locked_files.index(filename)
        return "File already locked."
    except ValueError:
        locked_files.append(filename)
        print(locked_files)
        return "Successfully locked file."


@app.route('/unlock', methods=['POST'])
def unlock():
    filename = request.form["filename"]
    try:
        file_index = locked_files.index(filename)
        del(locked_files[file_index])
        return("Successfully unlocked file.")
    except ValueError:
        return("Error: File is already unlocked or does not exist.")


@app.route('/lock_status', methods=['GET'])
def get_lock_status():
    filename = request.form["filename"]
    try:
        locked_files.index(filename)
        return "1"
    except ValueError:
        print("File is not locked.")
        return "0"

def main():
    app.run(port=config.lock_service_port)

main()
