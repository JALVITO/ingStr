#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Para que entienda acentos

import socket

# For compatibility with python 2 and 3
try:
    input = raw_input
except NameError:
    pass

IPservidor = input("Dirección del servidor: ")
PUERTOservidor = 5000
mensaje = " "
str_respuesta = " "

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nombre = input("Nombre de jugador: ")
s.sendto(nombre.encode('utf-8'), (IPservidor, PUERTOservidor))

while mensaje != "quit":

    while str_respuesta != "Your turn":
        respuesta = s.recv(1024)
        str_respuesta = respuesta.decode('utf-8')

    print(str_respuesta)

    while mensaje != "endTurn":
        respuesta = s.recv(1024)
        str_respuesta = respuesta.decode('utf-8')
        print(str_respuesta)
        mensaje = input("Query: ")
        s.sendto(mensaje.encode('utf-8'), (IPservidor, PUERTOservidor))

    mensaje = " "

s.close()
