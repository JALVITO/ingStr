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
respuesta = " "

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nombre = input("Nombre de jugador: ")
s.sendto(('player ' + nombre), (IPservidor, PUERTOservidor))

while mensaje != "quit":

	while respuesta != "Your turn"
		respuesta = s.recv(1024)

	print(respuesta)

	while mensaje != "endTurn"
		respuesta = s.recv(1024)
		print(respuesta)
	    mensaje = input("Query: ")
	    s.sendto(mensaje, (IPservidor, PUERTOservidor))

s.close()
