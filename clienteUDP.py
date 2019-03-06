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

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nombre = input("Nombre de jugador: ")
s.sendto(('player ' + nombre), (IPservidor, PUERTOservidor))

while mensaje != "quit":
    mensaje = input("query: ")
    s.sendto(mensaje, (IPservidor, PUERTOservidor))

    respuesta = s.recv(1024)
    print(respuesta)

s.close()
