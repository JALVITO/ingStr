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
str_response = " "

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

name = input("Nombre de jugador: ")
s.sendto(name.encode('utf-8'), (ip_server, server_port))
print(s.recv(1024).decode('utf-8'))

while message != "quit" and str_response != "endGame":

    while str_response != "Your turn" and str_response != "Ending game...":
        response = s.recv(1024)
        str_response = response.decode('utf-8')

    print(str_response)
    if str_response == "Ending game...":
        break

    response = s.recv(1024)
    str_response = response.decode('utf-8')
    print(str_response)

    while message != "endTurn":
        message = input("Query: ")
        s.sendto(message.encode('utf-8'), (ip_server, server_port))
        response = s.recv(1024)
        str_response = response.decode('utf-8')
        print(str_response)

        response = s.recv(1024)
        str_response = response.decode('utf-8')
        if str_response == "end" or str_response == "endGame":
            break

    message = " "

response = s.recv(1024)
str_response = response.decode('utf-8')
print(str_response)

s.close()
