import os
import requests
import json
import playerclass
from PIL import Image
from io import BytesIO
import random

def get_tag(ign):
    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()

    for player in playerlist.players:
        if ign == player.ign:
            return player.tag
    
    return False

def get_mmr_history(ign, tag=""):

    if tag == "":
        tag = get_tag(ign)
        if not tag:
            return False
    
    url = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{ign}/{tag}"

    headers = {'accept': 'application/json'}
    r = requests.get(url, headers=headers)

    if str(r) != "<Response [200]>":
        return False

    john = json.loads(r.text)

    if 'status' in john:
        if john['status'] == 429:
            return "welp"
        
        elif john['status'] == 404:
            return "User not found"
        
        elif john['status'] == 500:
            return "No matches available"
        
        elif john['status'] == 403:
            return "riot servers are down at the moment"
        
        elif john['status'] != 200:
            return False
    
    elif 'statusCode' in john:
        if john['statusCode'] == 429:
            return "welp"
        
        elif john['statusCode'] == 404:
            return "User not found"
        
        elif john['statusCode'] == 500:
            return "No matches available"
        
        elif john['statusCode'] != 200:
            return False

    if john['name'] == None or john['tag'] == None or ('error' in john.keys()):
        return False

    return john

def get_file_mmr(ign):

    file_path = f'elo_history/{ign}.txt'

    if os.path.isfile(file_path) == False:
        return False

    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()

    if lines[-1] == '\n':
        return False

    #return the latest MMR value in file
    return int(lines[-1].split(',')[0])

def initialise_file(ign):

    f = open(f'elo_history/{ign}.txt', "x")
    f.close()

    f = open(f'elo_history/{ign}.txt', "w")
    f.writelines('\n')
    f.close()

def update_database(ign, tag=""):

    if tag == "":
        tag = get_tag(ign)
        if not tag:
            return False
    
    player_data = get_mmr_history(ign, tag)

    if type(player_data) != dict:
        return player_data
    
    player_file_path = f'elo_history/{ign}.txt'

    if os.path.isfile(player_file_path) == False:
        if len(player_data['data']) == 0:
            return False
        else:
            initialise_file(ign)
    
    # Dates of last update
    date_raw = player_data["data"][0]["date_raw"]

    player_file = open(player_file_path, 'r')
    first_line = player_file.readline()
    
    if first_line == '\n':
        last_file_update = 0
    else:
        last_file_update = int(first_line)
    
    player_file.close()

    new_list = []

    if last_file_update == 0:

        for i in range(0, len(player_data['data'])):
            thedate = player_data['data'][i]['date'].replace(',', '-').replace(' ', '-').replace('--', '-')
            new_list.append(str(player_data['data'][i]['elo']) + ',' + thedate)


    elif len(str(last_file_update)) == 13:
        
        if (len(str(date_raw)) == 10):
            last_file_update = int(str(last_file_update)[:-3])
            last_num = int(str(last_file_update)[-1])
            last_num += 1
            last_file_update = int(str(last_file_update)[:-1] + str(last_num))

        for i in range(0, len(player_data['data'])):

            date_raw = player_data['data'][i]['date_raw']

            if last_file_update < date_raw:
                thedate = player_data['data'][i]['date'].replace(',', '-').replace(' ', '-').replace('--', '-')
                new_list.append(str(player_data['data'][i]['elo']) + ',' + thedate)

            else:
                break
    
    else:
        for i in range(0, len(player_data['data'])):

            date_raw = player_data['data'][i]['date_raw']

            if last_file_update < date_raw:
                thedate = player_data['data'][i]['date'].replace(',', '-').replace(' ', '-').replace('--', '-')
                new_list.append(str(player_data['data'][i]['elo']) + ',' + thedate)

            else:
                break
    
    if new_list != []:
        new_list = new_list[::-1]

        #update timestamp in file
        with open(player_file_path) as f:
            lines = f.readlines()
        
        lines[0] = str(player_data["data"][0]["date_raw"]) + '\n'

        with open(player_file_path, "w") as f:
            f.writelines(lines)

        player_file = open(player_file_path, 'a')
        
        for elem in range(0, len(new_list)):
            player_file.writelines(str(new_list[elem]) + '\n')

        player_file.close()
    
    return len(new_list)

def get_elo_list(ign):
    
    tag = get_tag(ign)
    if not tag:
        return "Player not found"

    update_database(ign, tag)

    if not get_file_mmr(ign):
        return "Player not found"
    
    file1 = open(f'elo_history/{ign}.txt', 'r')

    lines = [x.strip() for x in file1.readlines()]

    if len(lines) == 1:
        return "No comp games recorded"
        
    lines.pop(0)
    
    elolist = ""

    for elem in lines:
        elolist += elem.split(',')[0] + ", "

    return elolist[:-2]

def local_leaderboard():

    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()

    players = []

    for player in playerlist.players:

        mmr = get_file_mmr(player.ign)

        if type(mmr) == int:
            players.append((player.ign, mmr))
        
    players.sort(key=lambda x:x[1], reverse=True)

    leaderboard = "Player Leaderboard\n"

    for i in range(0, len(players)):

        ign = players[i][0]
        mmr = players[i][1]
        rank = i + 1
        leaderboard += (str(rank) + '.').ljust(3) + str(ign).ljust(16) + str(mmr).rjust(5) + '\n'

    f = open("leaderboard.txt", "w")
    f.write(leaderboard)
    f.close()

    return leaderboard

def region_leaderboard(region, length=20):

    url = f"https://api.henrikdev.xyz/valorant/v1/leaderboard/{region}"
    
    headers = {'accept': 'application/json'}
    r = requests.get(url, headers=headers)

    if str(r) == "<Response [204]>":
        return False

    regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}
    data = json.loads(r.text)
    players = []
    
    for i in range(length):
        if data[i]['IsAnonymized'] == True:
            players.append(("Anonymous", data[i]['rankedRating']))
        else:
            players.append((data[i]['gameName'], data[i]['rankedRating']))


    leaderboard = f'{regions[region]} Ranked Leaderboard\n'
    
    for i in range(0, len(players)):

        ign = players[i][0]
        mmr = players[i][1]
        rank = i + 1
        leaderboard += (str(rank) + '.').ljust(3) + str(ign).ljust(16) + str(mmr).rjust(5) + '\n'

    return leaderboard    

def stats(ign, tag=""):

    if tag == "":
        tag = get_tag(ign)
        if not tag:
            return "Player not found, check syntax: (username#tag)"

    url = f'https://api.henrikdev.xyz/valorant/v2/mmr/ap/{ign}/{tag}'
    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return "Player not found"

    john = json.loads(r.text)

    if john['status'] == '404' or john['status'] == '500':
        return "Player not found, check syntax: (username#tag)"
    
    data =  john['data']['by_season']

    keys = data.keys()
    final = []

    for key in keys:
        if 'error' in data[key].keys():
            final.append([f'Episode {key[1]} Act {key[3]}', "No data Available\n"])
        else:
            wins = data[key]['wins']
            games = data[key]['number_of_games']
            rank = data[key]['final_rank_patched']
            final.append([f'Episode {key[1]} Act {key[3]}:', f'{rank}\nGames Played: {games}\nWinrate: {round((wins/games) * 100, 2)}%'])
    
    url = f'https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}'
    r = requests.get(url)
    john = json.loads(r.text)
    card = john['data']['card']['small']

    return [final, card]

def get_banner(ign, tag):

    url = f'https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}'
    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return "Player not found"

    data = json.loads(r.text)

    if data['status'] != '200':
        return "Player not found, check syntax: (ign#tag)"
    
    url = data['data']['card']['large']
    r = requests.get(url, allow_redirects=True)

    open('banner.png', 'wb').write(r.content)

    return True

def account_check(ign, tag):

    url = f'https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}'

    headers = {'accept': 'application/json'}
    r = requests.get(url, headers=headers)

    if str(r) == "<Response [204]>":
        return False

    data = json.loads(r.text)

    if 'status' in data and (data['status'] == '404'):
        return False
    
    if 'statusCode' in data and (data['statusCode'] != 404):
        return False

    return True

def servercheck():

    counter = 0
    report = ""
    regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}

    for elem in regions.keys():
        
        url = f'https://api.henrikdev.xyz/valorant/v1/status/{elem}'

        headers = {'accept': 'application/json'}
        r = requests.get(url, headers=headers)

        if str(r) == "<Response [204]>":
            break

        john = json.loads(r.text)

        if 'status' in john:
            if type(john['status']) == str and john['status'] != '200':
                break
            
            if type(john['status']) == int and john['status'] != 200:
                break
        
        if 'statusCode' in john:
            if type(john['statusCode']) == str and john['statusCode'] != '200':
                break
            
            if type(john['statusCode']) == int and john['statusCode'] != 200:
                break
        

        maintenances = len(john['data']['maintenances'])
        incidents = len(john['data']['incidents'])
        counter += maintenances + incidents

        report += f'{regions[elem]}:\nMaintenances - {maintenances}\nIncidents - {incidents}\n'
        report += f'{regions[elem]}:\n{maintenances} maintenances and {incidents} incidents\n'

    if counter == 0:
        return "no maintenances or incidents reported"
        
    return report

def add_player(ign, tag):

    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()

    if not account_check(ign, tag):
        return "Account does not exist"

    player = playerclass.Player(ign.lower(), tag.lower())

    if playerlist.inList(player):
        return "Account already added"
    
    playerlist.add(player)
    playerlist.save()

    return f'{ign}#{tag} successfully added'

def remove_player(ign, tag):

    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()

    player = playerclass.Player(ign.lower(), tag.lower())

    if not playerlist.inList(player):
        return "Player not in list"
        
    playerlist.remove(player)
    playerlist.save()

    return f'{ign}#{tag} has been removed'

def crosshair(code):
    
    url = f"https://api.henrikdev.xyz/valorant/v1/crosshair/generate?id={code}"

    headers = {'accept': 'application/json'}
    r = requests.get(url, headers=headers)

    img = Image.open(BytesIO(r.content))
    img = img.save("crosshair.png")

    return True

def random_crosshair():

    crosshairs = {  "Reyna Flash" : "0;P;c;6;t;6;o;0.3;f;0;0t;1;0l;5;0o;5;0a;1;0f;0;1t;10;1l;4;1o;5;1a;0.5;1m;0;1f;0", 
                    "Windmill"    : "0;P;c;1;t;6;o;1;d;1;z;6;a;0;f;0;m;1;0t;10;0l;20;0o;20;0a;1;0m;1;0e;0.1;1t;10;1l;10;1o;40;1a;1;1m;0",
                    "Flappy Bird" : "0;P;c;1;t;3;o;1;f;0;0t;6;0l;20;0o;13;0a;1;0f;0;1t;9;1l;4;1o;9;1a;1;1m;0;1f;0",
                    "Flower"      : "0;P;c;6;o;1;d;1;z;4;f;0;m;1;0t;8;0l;3;0o;2;0a;0;0f;0;1l;3;1o;3;1a;0;1m;0;1f;0",
                    "Diamond"     : "0;P;c;5;h;0;f;0;0t;1;0l;3;0o;0;0a;1;0f;0;1t;3;1o;0;1a;1;1m;0;1f;0",
                    "Smiley"      : "0;P;c;7;t;2;o;1;d;1;z;3;a;0;f;0;0t;10;0l;2;0o;2;0a;1;0f;0;1b;0",
                    "Globe"       : "0;P;o;1;f;0;0t;10;0l;4;0a;0;0f;0;1t;4;1o;6;1a;0;1m;0;1f;0",
                    "Shuriken"    : "0;P;c;7;h;0;f;0;0l;4;0o;2;0a;1;0f;0;1t;8;1l;1;1o;1;1a;1;1m;0;1f;0",
                    "Fishnet"     : "0;P;o;1;d;1;a;0;f;0;0t;8;0l;2;0o;5;0a;0;0f;0;1l;8;1o;2;1a;0;1m;0;1f;0"}

    name, code = random.choice(list(crosshairs.items()))

    if not crosshair(code):
        return (False, False)

    return (name, code)

if __name__ == '__main__':
    print(update_database('lol'))
    #print(get_elo_list('oshawott'))
    #print(get_mmr_history("oshawott"))
    #print(local_leaderboard())
