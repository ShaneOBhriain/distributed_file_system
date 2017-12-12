python3 ./FileServer.py 8001 &
python3 ./FileServer.py 8002 &
python3 ./FileServer.py 8003 &
python3 ./lock_service.py &
python3 ./directory_service.py &
xterm -e python3 ./client.py
