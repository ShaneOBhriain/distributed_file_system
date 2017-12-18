# distributed_file_system

This project implements the following:

- Distributed Transparent File Access (Client)
- Directory Service
- Replication
- Caching
- Lock Service

The program can be run using "./start.sh"

The client is a command line interface offering the following options:

--------------------
1. Specify download folder. (set_download_folder 'filename')
2. Upload file. (upload 'filename')
3. Download file. (download 'filename')
4. Delete File (del 'filename') 
5. List directories. (ls)
6. Lock Operations on File (lock/unlock/locked 'filename')
--------------------

Downloading and uploading work as expected. 
Downloading will first check if the file is locked (via the lock service) and will only allow download if the file is not locked.
Before downloading, the file will also be checked to see if it was modified since the last time it was downloaded by the client - if not the cached version of the file will be used by the client.

To set a download folder other than the current working directory the command is set_download folder "new folder name".

The directory service enables replication by distributing the uploaded file to each of the file servers. It also enables the "ls" function which displays a directory tree of the files to the client.

The lock server allows locking and unlocking of files, as well as checking the lock status of a file. In principle if the client enabled live editing of files, files would be automatically locked using the lock service, then unlocked upon saving changes to the file.


