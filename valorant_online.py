import requests
import json

players = [ 
    ["Fakinator", "4269"],
    ["8888", "nadi"], 
    ["dilka30003", "0000"],
    ["slumonaire", "oce"]
    ]

all_data = {}

def get_all_data():
    global all_data
    for i in range(0, len(players)):
        url = "https://api.henrikdev.xyz/valorant/v1/live-match/{}/{}".format(players[i][0], players[i][1])
        r = requests.get(url, headers={'Cache-Control': 'no-cache'})
        all_data[players[i][0]] = json.loads(r.text)


def get_data(username, tagline):
    url = "https://api.henrikdev.xyz/valorant/v1/live-match/{}/{}".format(username, tagline)
    r = requests.get(url)
    return json.loads(r.text)

def get_status(username):
    data = all_data[username]
    status = ""
    if data['status'] == '200':
        state = data['data']['current_state']
        if state == 'PREGAME':
            status = "Online and in agent select"
        if state == 'MENUS':
            status = "Online and in menu"
        if state == 'INGAME':
            game_mode = data['data']['gamemode']
            score = str(data['data']['score_ally_team']) + '-' + str(data['data']['score_enemy_team'])
            map = data['data']['map']
            status = "Online in " + game_mode + " going " + score + " on " + map
    else:
        status = "Offline"
    
    return status

def get_party(username):
    data = all_data[username]
    if get_status(username) == "Offline":
        return
    return data['data']['party_id']

def form_partys():

    for i in range(0, len(players)):
        party_id = get_party(players[i][0])
        players[i].append(party_id)
    
    players.sort(key=lambda x: str(x[2]))

    count = 0
    parties = []
    a_party_id = players[0][2]
    

    while a_party_id != None and count < len(players):
        temp = []
        while a_party_id == players[count][2]:
            temp.append(players[count][0])
            count += 1
            if count == len(players):
                break
        
        if count != len(players):
            a_party_id = players[count][2]
        parties.append(temp)

    return parties

def everything():

    parties = form_partys()
    final = []
    
    for i in range(0, len(players)):
        final.append((players[i][0], get_status(players[i][0])))
    
    if len(parties) == 0:
        final.append(("no parties", ""))
        return final

    for i in range(0, len(parties)):
        final.append((("party" + str(i)), parties[i]))

    return final

#{'status': '200', 'data': {'custom_game': False, 'gamemode': 'unrated', 'current_state': 'INGAME', 
# 'party_accessibility': 'CLOSED', 'client_version': 'release-02.11-shipping-9-567060', 
# 'map': 'Split', 'score_ally_team': 12, 'score_enemy_team': 12, 'queue_entry_time': '2021.06.10-08.42.38', 'party_id': 'f75696dd-6295-4368-9a90-6bfb35544a1c'}}

'''
    #print(players)

    players = [ 
    ["Fakinator", "4269", "4555982f-e7d1-4ee2-beed-e7c0fcc0c59d"],
    ["8888", "nadi", "4555982f-e7d1-4ee2-beed-e7c0fcc0c595"], 
    ["dilka30003", "0000", "4555982f-e7d1-4ee2-beed-e7c0fcc0c595"],
    ["slumonaire", "oce", "4555982f-e7d1-4ee2-beed-e7c0fcc0c59d"]
    ]

    players.sort(key=lambda x: str(x[2]))
    print(players)
'''