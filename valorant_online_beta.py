import requests
import json
import playerlist

players = playerlist.classyplayers
all_data = {}

def get_all_data():
    global all_data
    all_data = {}
    
    for person in players:

        if person.online == False:
            continue

        url = "https://api.henrikdev.xyz/valorant/v1/live-match/{}/{}".format(person.ign, person.tag)
        r = requests.get(url, headers={'Cache-Control': 'no-cache'})
        all_data[person.ign] = json.loads(r.text)

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

        elif state == 'MENUS':
            status = "Online and in menu"

        elif state == 'INGAME':
            map = data['data']['map']

            if map == 'Range':
                status = "Online in the range"

            else:
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
        return None

    return data['data']['party_id']

def form_partys():

    party_players = []
    j = 0

    for i in range(0, len(players)):
        party_id = get_party(players[i].ign)

        if party_id != None:

            party_players.append([players[i].ign, players[i].tag])
            party_players[j].append(party_id)
            j += 1
    
    party_players.sort(key=lambda x: str(x[-1]))

    count = 0
    parties = []

    if party_players != []:
        a_party_id = party_players[0][-1]

    while count < len(party_players):
        temp = []

        while a_party_id == party_players[count][-1]:
            temp.append(playerlist.get_attribute(party_players[count][0], "name"))
            count += 1

            if count == len(party_players):
                break
        
        if count != len(party_players):
            a_party_id = party_players[count][-1]

        parties.append(temp)

    return parties

def everything():

    parties = form_partys()
    final = [("Players Online:", "")]

    for i in range(0, len(players)):
        entry = (players[i].name.ljust(8), get_status(players[i].ign))

        if entry[1] != "Offline":
            final.append(entry)

    if len(final) == 1:
        final.append(("All players offline", ""))

    final.append(("Parties:", ""))

    if len(parties) == 0:
        final.append(("no parties", ""))
        return final

    for i in range(0, len(parties)):

        randos = 0
        user = playerlist.get_attribute(parties[i][0], "ign")

        if all_data[user]['data']['current_state'] == 'MENUS' and len(parties[i]) < all_data[user]['data']['party_size']:
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