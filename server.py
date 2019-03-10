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
    cont = 0
    for word in play_field:
        l1 = "   0"
        l2 = "             "

        if len(word) > 5:
            l1 += "    5"
            if len(word) > 10:
                for x in range(11, len(word), 5):
                    l1 += "    " + str(int(x/10))
                    l2 += str((x-1) % 10) + "    "

        s += "{:0>2}".format(cont) + " " + word + "\n" + l1 + "\n" + l2 + "\n"
        cont += 1
    return s


def analyze_data(data):
    if "substring" in data:
        if (len(data) == 4 and 0 <= int(data[1]) < len(play_field) and
                0 <= int(data[2]) < len(play_field[int(data[1])]) and
                0 <= int(data[3]) < len(play_field[int(data[1])]) and
                int(data[2]) <= int(data[3])):
            substring(int(data[1]), int(data[2]), int(data[3]))
            return True
        else:
            return False
    elif "concat" in data:
        if (len(data) == 3 and 0 <= int(data[1]) < len(play_field) and
                0 <= int(data[2]) < len(play_field)):
            concat(int(data[1]), int(data[2]))
            return True
        else:
            return False
    elif "reverse" in data:
        if len(data) == 2 and 0 <= int(data[1]) < len(play_field):
            reverse(int(data[1]))
            return True
        else:
            return False
    elif "identify" in data:
        if len(data) == 2 and 0 <= int(data[1]) < len(play_field):
            is_valid(data[1])
            return True
        else:
            return False
    elif "end" in data:
        end_game()
        return True
    else:
        return False


def add_player(ip, name):
    players.append({"ip": ip, "name": name, "words": []})


def substring(word_id, low_bound, up_bound):
    play_field.append(play_field[word_id][low_bound:up_bound+1])
    play_field[word_id] = play_field[word_id][0:low_bound] + play_field[word_id][up_bound+1:len(play_field[word_id])]
    return


def concat(word1_id, word2_id):
    new_word = play_field[word1_id] + play_field[word2_id]
    if word1_id == word2_id:
        return
    elif word1_id < word2_id:
        play_field.pop(word2_id)
        play_field.pop(word1_id)
    else:
        play_field.pop(word1_id)
        play_field.pop(word2_id)
    play_field.append(new_word)
    return


def reverse(word_id):
    play_field[word_id] = play_field[word_id][::-1]
    return


def is_valid(word):
    uri_entry = 'https://od-api.oxforddictionaries.com/api/v1/entries/'
    uri_lemmatron = 'https://od-api.oxforddictionaries.com/api/v1/inflections/'
    uris = [uri_entry, uri_lemmatron]
    for uri in uris:
        uri += language + '/' + word
        r = requests.get(uri, headers=headers)
        if r.status_code == 200:
            return True
    return False


def identify(word_id):
    if is_valid(play_field[word_id]):
        print("It exists")
    else:
        print("It doesn't exists")
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
    s.sendto("Connected to server".encode('utf-8'), players[0]["ip"])

    # Add Player 2
    datos, address = s.recvfrom(1024)
    str_datos = datos.decode('utf-8')
    add_player(address, str_datos)
    print(players[1])
    s.sendto("Connected to server".encode('utf-8'), players[1]["ip"])

    while True:
        str_datos = " "
        success = True
        s.sendto("Your turn".encode('utf-8'), players[0]["ip"])
        while str_datos != "endTurn":
            if (success):
                s.sendto(build_field_string().encode('utf-8'), players[0]["ip"])
            else:
                s.sendto("Query invalido \n".encode('utf-8'), players[0]["ip"])

            datos, address = s.recvfrom(1024)
            str_datos = datos.decode('utf-8')

            print(address[0] + " sent: " + str_datos)
            success = analyze_data(str_datos.split())

        str_datos = " "
        success = True
        s.sendto("Your turn".encode('utf-8'), players[1]["ip"])
        while str_datos != "endTurn":
            if (success):
                s.sendto(build_field_string().encode('utf-8'), players[1]["ip"])
            else:
                s.sendto("Query invalido \n".encode('utf-8'), players[1]["ip"])

            datos, address = s.recvfrom(1024)
            str_datos = datos.decode('utf-8')

            print(address[0] + " sent: " + str_datos)
            success = analyze_data(str_datos.split())

    s.close()


if __name__ == "__main__":
    main()
