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
s = None
movements = None


def init_connection():
    global s
    server_port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", server_port))


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


def analyze_data(data, player_id):
    global movements
    try:
        if "substring" in data:
            substring(int(data[1]), int(data[2]), int(data[3]))
            movements -= 1
        elif "concat" in data:
            concat(int(data[1]), int(data[2]))
            movements -= 1
        elif "reverse" in data:
            reverse(int(data[1]))
            movements -= 1
        elif "identify" in data:
            identify(int(data[1]), player_id)
        elif "end" in data:
            end_game()
        else:
            return False
        return True
    except IndexError:
        return False


def add_player(ip, name):
    players.append({"ip": ip, "name": name, "words": []})


def substring(word_id, low_bound, up_bound):
    word = play_field[word_id]
    play_field.append(word[low_bound:up_bound+1])
    play_field[word_id] = word[0:low_bound] + word[up_bound+1:]
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


def identify(word_id, player_id):
    if is_valid(play_field[word_id]):
        print("It exists")
        play_field.pop(word_id)
        players[player_id]["words"].append(play_field[word_id])
        return True
    print("It doesn't exists")
    return False


def end_game():
    return


def connect_player(player_id):
    # Add Player 1
    data, address = s.recvfrom(1024)
    str_data = data.decode('utf-8')
    add_player(address, str_data)
    print(players[player_id])
    s.sendto("Connected to server".encode('utf-8'), players[player_id]["ip"])


def player_turn(player_id):
    global movements
    str_data = " "
    success = True
    movements = 2
    s.sendto("Your turn".encode('utf-8'), players[player_id]["ip"])
    while str_data != "endTurn" and movements > 0:
        if (success):
            s.sendto(build_field_string().encode('utf-8'),
                     players[player_id]["ip"])
        else:
            s.sendto("Query invalido \n".encode('utf-8'),
                     players[player_id]["ip"])

        data, address = s.recvfrom(1024)
        str_data = data.decode('utf-8')

        print(address[0] + " sent: " + str_data)
        success = analyze_data(str_data.split(), player_id)


def main():
    try:
        create_string()
        init_connection()

        connect_player(0)
        connect_player(1)

        while True:
            player_turn(0)
            player_turn(1)

        s.close()
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    main()
