import configparser
from sys import flags
import requests
import json
import os

def playerlist():
    players = [("silentwhispers", "0000"), 
    ("Fakinator", "4269"), 
    ("faqinator", "7895"), 
    ("8888", "nadi"), 
    ("dilka30003", "0000"),
    ("slumonaire", "oce"),
    ("KATCHAMPION", "oce"), 
    ("imabandwagon", "oce"), 
    ("giroud", "8383"), 
    ("oshaoshawott", "oce"), 
    ("YoVivels", "1830"), 
    ("therealrobdez", "3333")]
    return players

def get_player_data(username, tagline):
    url = "https://api.henrikdev.xyz/valorant/v1/mmr/ap/{}/{}".format(username, tagline)
    r = requests.get(url)
    return r.text

def get_elos():

    players = playerlist()
    bohn = []

    for i in range(0, len(players)):
        if players[i][0] == "8888":
            bohn.append((69, players[i][0]))
            
        else:
            data = get_player_data(players[i][0], players[i][1])
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
        leaderboard += "{}. {} {}\n".format(rank, user, elo)

    return leaderboard

def get_elo_history(username, tagline):
    url = "https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{}/{}".format(username, tagline)
    r = requests.get(url)
    john = json.loads(r.text)

    return john

def make_elo_list(username, tagline):
    data = get_elo_history(username, tagline)
    elo_list = []
    
    for i in range(0, len(data['data'])):
        elo_list.append(data['data'][i]['elo'])
    
    return elo_list

def initialise_file(username):

    f = open('elo_history/{}.txt'.format(username), "x")
    f.close()
    f = open('elo_history/{}.txt'.format(username), "w")
    f.writelines(str(0) + '\n')
    f.close()

    return

def update_elo_history(username, tagline):

    player_file_path = 'elo_history/{}.txt'.format(username)

    if os.path.isfile(player_file_path) == False:
        initialise_file(username)

    player_data = get_elo_history(username, tagline)

    # Dates of last update
    date_raw = player_data["data"][0]["date_raw"]
    player_file = open(player_file_path, 'r')
    last_file_update = int(player_file.readline())
    player_file.close()

    new_elo_list = []
    i = 0

    if last_file_update == 0:
        for i in range(0, len(player_data['data'])):
            new_elo_list.append(player_data['data'][i]['elo'])

    else:
        while last_file_update < date_raw:
            
            new_elo_list.append(player_data['data'][i]['elo'])
            if last_file_update != date_raw:
                i += 1
            date_raw = player_data['data'][i]['date_raw']

    correctly_sorted_new_elo_list = new_elo_list[::-1]

    player_file = open(player_file_path, 'a')
    
    for elem in range(0, len(correctly_sorted_new_elo_list)):
        player_file.writelines(str(correctly_sorted_new_elo_list[elem]) + '\n')

    player_file.close()

    #update timestamp in file
    with open(player_file_path) as f:
        lines = f.readlines()
    lines[0] = str(player_data["data"][0]["date_raw"]) + '\n'
    with open(player_file_path, "w") as f:
        f.writelines(lines)   
    
    return

def update_all_elo_history():

    players = playerlist()
    for i in range(0, len(players)):
        update_elo_history(players[i][0], players[i][1])

    return

print(get_elo_history("YoVivels", "1830"))