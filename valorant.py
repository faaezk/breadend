import configparser
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

def earliest_elo_update(username, tagline):
    data = get_elo_history(username, tagline)

    return data["data"][-1]["date_raw"]

def initialise_file(username, tagline):

    f = open('elo_history/{}.txt'.format(username), "x")
    f.close()
    f = open('elo_history/{}.txt'.format(username), "w")
    f.writelines(str(earliest_elo_update(username, tagline)))
    f.close()

    return

def update_elo_history(username, tagline):

    player_file_path = 'elo_history/{}.txt'.format(username)
    first_time = False
    if os.path.isfile(player_file_path) == False:
        initialise_file(username, tagline)
        first_time = True

    current_elo_list = make_elo_list(username, tagline)
    player_data = get_elo_history(username, tagline)

    # Dates of last update
    date_raw = player_data["data"][0]["date_raw"]
    player_file = open(player_file_path, 'r')
    latest_game = int(player_file.readline())
    player_file.close()

    print(date_raw)
    print(latest_game)

    new_elo_list = []
    i = 0

    #if first_time == True:
    #    new_elo_list.append(player_data['data'][i]['elo'])
    print("john")
    while latest_game <= date_raw:
        
        new_elo_list.append(player_data['data'][i]['elo'])
        date_raw = player_data['data'][i]['date_raw']
        if latest_game != date_raw:
            i += 1

    correctly_sorted_new_elo_list = new_elo_list[::-1]

    player_file = open(player_file_path, 'a')
    
    for elem in range(0, len(correctly_sorted_new_elo_list)):
        print(elem)
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

print(update_elo_history("Fakinator", "4269"))
print(make_elo_list("Fakinator", "4269"))
print(get_elo_history("Fakinator", "4269"))