import requests
import json
import os
from datetime import datetime

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
    ("therealrobdez", "3333"),
    ("bento2", "box"), 
    ("hoben222", "9327"), 
    ("jokii", "oce")]

def get_elo_history(username, tagline):
    
    url = "https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{}/{}".format(username, tagline)
    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return False

    john = json.loads(r.text)

    return john

def initialise_file(username):

    f = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), "x")
    f.close()
    f = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), "w")
    f.writelines(str(0) + '\n')
    f.close()

    return

def update_elo_history(username, tagline):

    player_data = get_elo_history(username, tagline)
    if player_data == False:
        return 0
    
    player_file_path = '/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username)

    if os.path.isfile(player_file_path) == False:
        initialise_file(username)

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
    
    return len(correctly_sorted_new_elo_list)

def update_all_elo_history():
    update_count = 0
    for i in range(0, len(players)):
        update_count += update_elo_history(players[i][0], players[i][1])
        #print("completed " + str(i + 1) + "/" + str(len(players)))

    return str(update_count) + " updates"

updates = update_all_elo_history()
now = datetime.now()
print("completed on: " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S") + " with " + updates)