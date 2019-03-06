#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Para que entienda acentos

import socket
import random
import bisect

playField = [""]
players = []


def initConnection():
    PUERTOservidor = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PUERTOservidor))
    return s


def createString():
    letters = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'D', 'L', 'U', 'C',
               'M', 'F', 'Y', 'W', 'G', 'P', 'B', 'V', 'K', 'X', 'Q', 'J', 'Z']
    prob = [0.1202, 0.2112, 0.2924, 0.3692, 0.4423, 0.5118, 0.5746, 0.6348,
            0.6940, 0.7372, 0.7770, 0.8058, 0.8329, 0.8590, 0.8820, 0.9031,
            0.9240, 0.9443, 0.9625, 0.9774, 0.9885, 0.9954, 0.9971, 0.9982,
            0.9992, 1.0000]

    for x in range(30):
        num = random.random()
        playField[0] += letters[bisect.bisect(prob, num)]


def printField(s):
    for word in playField:
        # s.sendall(word)
        # print(word)

        l1 = "0"
        l2 = "          "

        if len(word) > 5:
            l1 += "    5"
            if len(word) > 10:
                for x in range(11, len(word), 5):
                    l1 += "    " + str(x/10)
                    l2 += str((x-1) % 10) + "    "

        # s.sendall(l1)
        # s.sendall(l2)
        # print(l1)
        # print(l2)


def analyzeData(data, ip):
    if 'player' in data:
        add_player(ip, data[1])
    elif 'substring' in data:
        substring(int(data[1]), int(data[2]), int(data[3]))
    elif 'concat' in data:
        concat(int(data[1]), int(data[2]))
    elif 'reverse' in data:
        reverse(int(data[1]))
    elif 'identify' in data:
        identify(int(data[1]))
    elif 'end' in data:
        end_game()
    # else:
        # s.sendall("Query no valido. Intente otra vez")


def add_player(ip, name):
    players.append({'ip': ip, 'name': name, 'words': []})


def substring(low_bound, up_bound, other):
    return


def concat(word1_id, word2_id):
    return


def reverse(word_id):
    return


def identify(word_id):
    return


def end_game():
    return


def main():
    createString()
    s = initConnection()

    while True:
        datos, address = s.recvfrom(1024)
        print(address[0] + " sent: " + datos)
        analyzeData(datos.split(), address)

        # printField(s)
        for p in players:
            s.sendto("hi", p['ip'])

    s.close()


if __name__ == '__main__':
    main()
