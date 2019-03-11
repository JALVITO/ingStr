#!/usr/bin/env python
# -*- coding: utf-8 -*-
# To understand special characters

import socket

# For compatibility with python 2 and 3
try:
    input = raw_input
except NameError:
    pass

ip_server = input("Dirección del servidor: ")
server_port = 5000
message = " "
str_reponse = " "

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

name = input("Nombre de jugador: ")
s.sendto(name.encode('utf-8'), (ip_server, server_port))
print(s.recv(1024).decode('utf-8'))

while message != "quit":

    while str_reponse != "Your turn":
        repose = s.recv(1024)
        str_reponse = repose.decode('utf-8')

    print(str_reponse)

    while message != "endTurn":
        repose = s.recv(1024)
        str_reponse = repose.decode('utf-8')
        print(str_reponse)
        message = input("Query: ")
        s.sendto(message.encode('utf-8'), (ip_server, server_port))

    message = " "

s.close()
