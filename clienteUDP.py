#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Para que entienda acentos

import socket

IPservidor = raw_input("Dirección del servidor: ")
PUERTOservidor = 5000
mensaje = " "

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nombre = raw_input("Nombre de jugador: ")
s.sendto(('player ' + nombre), (IPservidor, PUERTOservidor))

while mensaje != "quit":
	mensaje = raw_input("query: ")
	s.sendto(mensaje, (IPservidor, PUERTOservidor))	

	respuesta = s.recv(1024)
	print respuesta

s.close()