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
gameRunning = True


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
    field = ""
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

        field += "{:0>2}".format(cont) + " " + word
        field += "\n" + l1 + "\n" + l2 + "\n"
        cont += 1
    return field


def analyze_data(data, player_id):
    global movements
    try:
        if "substring" in data and int(data[2]) <= int(data[3]):
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
            movements -= 1
        elif "end" in data:
            end_game(player_id)
        elif "end_turn" in data:
            movements = 0
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
        players[player_id]["words"].append(play_field[word_id])
        play_field.pop(word_id)
        return True
    print("It doesn't exists")
    return False


def score(player_id):
    current_sum = 0
    for word in players[player_id]["words"]:
        current_sum += len(word)
    return current_sum


def game_tie():
    players[0]["words"].sort(key=len, reverse=True)
    players[1]["words"].sort(key=len, reverse=True)

    word_amount = min(len(players[0]["words"]), len(players[1]["words"]))

    for i in range(0, word_amount):
        word_player1 = players[0]["words"][i]
        word_player2 = players[1]["words"][i]

        if len(word_player1) > len(word_player2):
            return players[0]["name"] + " won \n"
        elif len(word_player1) < len(word_player2):
            return players[1]["name"] + " won \n"

    return "Game is a tie \n"


def player_inventory(player_id):
    inventory = ''
    inventory += "\n" + players[player_id]["name"] + "'s inventory: \n"
    for word in players[player_id]["words"]:
        inventory += word + "\n"
    return inventory


def end_game(player_id):
    global gameRunning, movements
    result = ""
    score_player1 = score(0)
    score_player2 = score(1)

    if score_player1 > score_player2:
        result += players[0]["name"] + " won \n \n"
    elif score_player1 < score_player2:
        result += players[1]["name"] + " won \n \n"
    else:
        result += game_tie()

    result += player_inventory(0)
    result += player_inventory(1)

    s.sendto("Ending game...".encode('utf-8'), players[0]["ip"])
    s.sendto("endGame".encode('utf-8'), players[0]["ip"])
    s.sendto(result.encode('utf-8'), players[player_id]["ip"])
    s.sendto("Ending game...".encode('utf-8'), players[1]["ip"])
    s.sendto(result.encode('utf-8'), players[1]["ip"])

    gameRunning = False
    movements = 0
    return


def connect_player(player_id):
    data, address = s.recvfrom(1024)
    str_data = data.decode('utf-8')
    add_player(address, str_data)
    print(players[player_id])
    s.sendto("Connected to server".encode('utf-8'), players[player_id]["ip"])


def player_turn(player_id):
    global movements
    str_data = " "
    success = True
    movements = 3
    s.sendto("Your turn".encode('utf-8'), players[player_id]["ip"])
    s.sendto(build_field_string().encode('utf-8'), players[player_id]["ip"])

    while str_data != "endTurn" and movements > 0:
        data, address = s.recvfrom(1024)
        str_data = data.decode('utf-8')

        print(address[0] + " sent: " + str_data)
        success = analyze_data(str_data.split(), player_id)

        if (success):
            s.sendto(build_field_string().encode('utf-8'),
                     players[player_id]["ip"])
        else:
            s.sendto("Query invalido \n".encode('utf-8'),
                     players[player_id]["ip"])

        if movements > 0:
            s.sendto("cont".encode('utf-8'), players[player_id]["ip"])
        else:
            s.sendto("end".encode('utf-8'), players[player_id]["ip"])


def main():
    try:
        create_string()
        init_connection()

        connect_player(0)
        connect_player(1)

        while gameRunning:
            player_turn(0)
            if gameRunning:
                player_turn(1)

        s.close()
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    main()
