#!/usr/bin/env python
# -*- coding: utf-8 -*-
# To understand special characters

import socket
import random
import bisect
import requests
from os import environ

play_field = [""]
players = []
headers = {'app_id': environ.get('APP_ID'), 'app_key': environ.get('APP_KEY')}
language = 'en'
lex_category = '/lexicalCategory=suffix,noun,determiner,adverb,combining_form,idiomaticredeterminerarticle,residual,adjectiverepositionrefix,other,verb,numeral,conjunction,pronoun,interjection,contraction'


def init_connection():
    server_port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", server_port))
    return s


def create_string():
    letters = ["E", "T", "A", "O", "I", "N", "S", "R", "H", "D", "L", "U", "C",
               "M", "F", "Y", "W", "G", "P", "B", "V", "K", "X", "Q", "J", "Z"]
    prob = [0.1202, 0.2112, 0.2924, 0.3692, 0.4423, 0.5118, 0.5746, 0.6348,
            0.6940, 0.7372, 0.7770, 0.8058, 0.8329, 0.8590, 0.8820, 0.9031,
            0.9240, 0.9443, 0.9625, 0.9774, 0.9885, 0.9954, 0.9971, 0.9982,
            0.9992, 1.0000]

    for x in range(30):
        num = random.random()
        play_field[0] += letters[bisect.bisect(prob, num)]


def build_field_string():
    s = ""
    for word in play_field:
        l1 = "0"
        l2 = "          "

        if len(word) > 5:
            l1 += "    5"
            if len(word) > 10:
                for x in range(11, len(word), 5):
                    l1 += "    " + str(int(x/10))
                    l2 += str((x-1) % 10) + "    "

    s += word + "\n" + l1 + "\n" + l2 + "\n"
    return s


def analyze_data(data, ip):
    if "substring" in data:
        substring(int(data[1]), int(data[2]), int(data[3]))
    elif "concat" in data:
        concat(int(data[1]), int(data[2]))
    elif "reverse" in data:
        reverse(int(data[1]))
    elif "identify" in data:
        is_valid(data[1])
    elif "end" in data:
        end_game()
    # else:
        # s.sendall("Query no valido. Intente otra vez")


def add_player(ip, name):
    players.append({"ip": ip, "name": name, "words": []})


def substring(word_id, low_bound, up_bound):
    return


def concat(word1_id, word2_id):
    return


def reverse(word_id):
    return


def is_valid(word):
    uri_entry = 'https://od-api.oxforddictionaries.com/api/v1/entries/'
    uri_lemmatron = 'https://od-api.oxforddictionaries.com/api/v1/inflections/'
    uris = [uri_entry, uri_lemmatron]
    for uri in uris:
        uri += language + '/' + word + lex_category
        r = requests.get(uri, headers=headers)
        if r.status_code == 200:
            print('It does exists')
            return True
    print("It doesn't exists")
    return False


def identify(word_id):
    return


def end_game():
    return


def main():
    create_string()
    s = init_connection()

    # Add Player 1
    datos, address = s.recvfrom(1024)
    str_datos = datos.decode('utf-8')
    add_player(address, str_datos)
    print(players[0])

    # Add Player 2
    datos, address = s.recvfrom(1024)
    str_datos = datos.decode('utf-8')
    add_player(address, str_datos)
    print(players[1])

    while True:
        str_datos = " "
        s.sendto("Your turn".encode('utf-8'), players[0]["ip"])
        while str_datos != "endTurn":
            s.sendto(build_field_string().encode('utf-8'), players[0]["ip"])
            datos, address = s.recvfrom(1024)
            str_datos = datos.decode('utf-8')

            print(address[0] + " sent: " + str_datos)
            analyze_data(str_datos.split(), address)

            s.sendto(build_field_string().encode('utf-8'), players[1]["ip"])

        str_datos = " "
        s.sendto("Your turn".encode('utf-8'), players[1]["ip"])
        while str_datos != "endTurn":
            s.sendto(build_field_string().encode('utf-8'), players[1]["ip"])
            datos, address = s.recvfrom(1024)
            str_datos = datos.decode('utf-8')

            print(address[0] + " sent: " + str_datos)
            analyze_data(str_datos.split(), address)

            s.sendto(build_field_string().encode('utf-8'), players[0]["ip"])

    s.close()


if __name__ == "__main__":
    main()
