import requests
import json

players = [ 
    ["Fakinator", "4269"],
    ["8888", "nadi"], 
    ["dilka30003", "0000"],
    ["slumonaire", "oce"],
    ["Hoben222", "9327"],
    ["silentwhispers", "0000"],
    ["imabandwagon", "oce"]
    ]

names = {"Fakinator" : "Faaez", "8888" : "Hadi", "dilka30003" : "Dhiluka", 
        "slumonaire" : "Chris", "Hoben222" : "Ben", "silentwhispers" : "Rasindu",
        "imabandwagon" : "Dylan"}

all_data = {}
def get_all_data():
    global all_data
    all_data = {}
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
    if data['status'] == "500":
        return
    return data['data']['party_id']

def form_partys():

    for i in range(0, len(players)):
        party_id = get_party(players[i][0])
        players[i].append(party_id)
    
    players.sort(key=lambda x: str(x[-1]))
    players.reverse()
    print(players)
    count = 0
    parties = []
    a_party_id = players[0][2]

    while a_party_id != None and count < len(players):
        temp = []
        while a_party_id == players[count][2]:
            temp.append(names[players[count][0]])
            count += 1
            if count == len(players):
                break
        
        if count != len(players):
            a_party_id = players[count][2]
        parties.append(temp)

    return parties

def everything():

    parties = form_partys()
    final = [("Players:", "")]
    
    for i in range(0, len(players)):

        final.append((names[players[i][0]].ljust(8), get_status(players[i][0])))

    final.append(("Parties:", ""))

    if len(parties) == 0:
        final.append(("no parties", ""))
        return final

    for i in range(0, len(parties)):

        a_party = ""
        for player in parties[i]:
            a_party = a_party + player + ", "
        a_party = a_party[:-2]

        final.append((("Party " + str(i + 1)), a_party))

    return final

print(get_all_data())

print(everything())