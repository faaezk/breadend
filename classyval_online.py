import requests
import json
import playerlist

players = sorted(playerlist.classyplayers, key=lambda x: x.online, reverse=True)
all_data = {}
online_count = 0

def get_all_data():

    global all_data
    global online_count
    all_data = {}
    
    for person in players:
        if person.online == False:
            break

        online_count += 1

        url = "https://api.henrikdev.xyz/valorant/v1/live-match/{}/{}".format(person.ign, person.tag)
        r = requests.get(url, headers={'Cache-Control': 'no-cache'})
        all_data[person.ign] = json.loads(r.text)

    return

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
        return False

    return data['data']['party_id']

def form_parties():

    global online_count
    global all_data
    inparty = []

    for i in range(0, online_count):
        party_id = get_party(players[i].ign)

        if party_id == False:
            continue
        
        inparty.append([players[i].name, party_id])
    
    inparty.sort(key=lambda x: str(x[-1]))

    if inparty == []:
        return
    
    current_party = inparty[0][1]
    parties = []

    for i in range(0, len(inparty)):

        temp = []
        j = i

        while current_party == inparty[i][1]:
            temp.append(inparty[j][0])
            j += 1
            current_party == inparty[j][1]

        parties.append(temp)
        i = j - 1

    return parties

def main():

    parties = form_parties()
    final = []

    for i in range(0, online_count):
        status = get_status(players[i].ign)

        if status != "Offline":
            final.append(players[i].name.ljust(8), status)

    if final == []:
        final.append(("All players offline", ""))
        return final
    
    final.append(("Players Online", ""))
    final.append(("Parties:", ""))

    for i in range(0, len(parties)):

        randos = 0
        leader = playerlist.get_attribute(parties[i][0], "ign")
        party_size = len(parties[i])
        
        if all_data[leader]['data']['current_state'] == 'MENUS':    
            randos = all_data[leader]['data']['party_size'] - party_size

        temp = ""
        for player in parties[i]:
            temp = temp + player + ", "

        temp = temp[:-2]

        if randos == 1:
            temp += " (with " + str(randos) + " other person)"
        if randos > 1:
            temp += " (with " + str(randos) + " other people)"

        final.append((("Party " + str(i + 1)), temp))

        return final
