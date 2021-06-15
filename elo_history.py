import requests
import json
import os

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
    ("jokii", "oce"),
    ("Lyçhii", "mai"),
    ("lmao", "6548"),
    ("jack", "ytb"),
    ("VKj", "4084"),
    ("TallEwok", "6209"),
    ("Fade", "1280"),
    ("SkzCross", "OCE"),
    ("lol", "4529"),
    ("Crossaxis", "mippl"),
    ("Azatory", "nike")
    ]

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
        for i in range(0, len(player_data['data'])):
            date_raw = player_data['data'][i]['date_raw']
            if last_file_update < date_raw:
                new_elo_list.append(player_data['data'][i]['elo'])
            else:
                break
    
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

def get_elolist(username):

    tagline = ""
    for player in players:
        if player[0] == username:
            tagline = player[1]

    player_data = get_elo_history(username, tagline)
    if player_data == False:
        return 0

    player_file_path = '/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username)

    if os.path.isfile(player_file_path) == False:
        return "Player not found or hasn't played any comp games recently"
    
    with open(player_file_path) as f:
        lines = [line.rstrip() for line in f]
    
    lines = lines[1:]
    elolist = ""
    for elem in lines:
        elolist += elem + ", "

    return elolist[:-2]
