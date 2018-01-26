# simple time server

import socket
from datetime import datetime

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('localhost', 8087))
serversocket.listen(5)

while True:
    sock, address = serversocket.accept()
    buf = str(datetime.now())
    sock.send(buf.encode())  # .encode() to bytes, to send to the client
    sock.close()

serversocket.close()


