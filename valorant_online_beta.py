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

game_names = {"Faaez" : "Fakinator", "Hadi" : "8888", "Dhiluka" : "dilka30003", 
        "Chris" : "slumonaire", "Ben" : "Hoben222", "Rasindu" : "silentwhispers",
        "Dylan" : "imabandwagon"}

offline = {'party_id' : None}
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
    if data['status'] == '200' and data != offline: # I think the problem was here
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

#I think the problem was here
def get_party(username):
    data = all_data[username]
    if data['status'] == "500":
        data['data'] = offline
        print(str(username) + "data:")
        print(data)
        return None
    return data['data']['party_id']

def form_partys():
    local_players = players
    for i in range(0, len(local_players)):
        party_id = get_party(local_players[i][0])
        local_players[i].append(party_id)
    
    local_players.sort(key=lambda x: str(x[2]))
    local_players.reverse()
    print(local_players)
    count = 0
    parties = []
    a_party_id = local_players[0][2]

    while a_party_id != None:
        temp = []
        while a_party_id == local_players[count][2]:
            temp.append(names[local_players[count][0]])
            count += 1
            if count == len(local_players):
                break
        
        if count != len(local_players):
            a_party_id = local_players[count][2]
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
        randos = 0
        user = game_names[parties[i][0]]
        if all_data[user]['data']['current_state'] == 'MENUS' and len(parties[i]) != all_data[user]['data']['party_size']:
            randos = all_data[user]['data']['party_size'] - len(parties[i])
        
        a_party = ""
        for player in parties[i]:
            a_party = a_party + player + ", "
        a_party = a_party[:-2]

        if randos != 0:
            if randos == 1:
                a_party += " (with " + str(randos) + " other person)"
            else:
                a_party += " (with " + str(randos) + " other people)"

        final.append((("Party " + str(i + 1)), a_party))

    return final

#print(get_all_data())

#print(everything())

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