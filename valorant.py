import requests
import json
import playerlist

players = playerlist.players

def get_player_data(username, tagline):
    url = "https://api.henrikdev.xyz/valorant/v1/mmr/ap/{}/{}".format(username, tagline)
    r = requests.get(url)
    if r.text == "":
        return None
    return r.text

def get_elos():
    
    bohn = []

    for i in range(0, len(players)):
        data = get_player_data(players[i][0], players[i][1])
        if data == None:
            continue
        john = json.loads(data)
        bohn.append((john['data']['elo'], players[i][0]))

    return sorted(bohn, reverse=True)

def elo_leaderboard():

    bohn = get_elos()
    leaderboard = ""
    
    for i in range(0, len(bohn)):

        user = bohn[i][1]
        elo = bohn[i][0]
        rank = i + 1
        leaderboard += str(rank).ljust(3) + '.' + str(user).ljust(14) + str(elo).rjust(5) + '\n'

    return leaderboard