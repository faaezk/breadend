import math
import os
import requests
import json
import beta_playerclass
from PIL import Image
from io import BytesIO
import random
import configparser

def get_key():
    c = configparser.ConfigParser()
    c.read('config.ini')

    return c['henrik']['key']

def get_data(category, puuid="None", ign="", tag="", region="", crosshair_code=""):
    key = get_key()
    headers = {'accept' : 'application/json', 'Authorization' : key}
    errors = {1 : "Invalid API Key", 2 : "Forbidden endpoint", 3 : "Restricted endpoint", 101 : "No region found for this Player",
            102 : "No matches found, can't get puuid", 103 : "Possible name change detected, can't get puuid. Please play one match, wait 1-2 minutes and try it again",
            104 : "Invalid region", 105 : "Invalid filter", 106 : "Invalid gamemode", 107 : "Invalid map", 108 : "Invalid locale",
            109 : "Missing name", 110 : "Missing tag", 111 : "Player not found in leaderboard", 112 : "Invalid raw type",
            113 : "Invalid match or player id", 114 : "Invalid country code", 115 : "Invalid season", 429 : 'welp', 
            403 : 'Forbidden', 404 : 'User not found', 500 : 'No matches available'}

    if region != "":
        if category == "leaderboard":
            url = f"https://api.henrikdev.xyz/valorant/v1/leaderboard/{region}"
        
        if category == "status":
            url = f'https://api.henrikdev.xyz/valorant/v1/status/{region}'

    elif category == "crosshair":
        url = f"https://api.henrikdev.xyz/valorant/v1/crosshair/generate?id={crosshair_code}"
        return requests.get(url, headers=headers)

    else:
        if puuid != "None":
            if category == "account":
                url = f'https://api.henrikdev.xyz/valorant/v1/by-puuid/account/{puuid}'

            elif category == "mmr":
                url = f'https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/ap/{puuid}'

            elif category == "mmr history":
                url = f'https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr-history/ap/{puuid}'

        else:
            if ign == "":
                return (False, 'no ign or puuid given/player not in database')

            if tag == "":
                tag = get_tag(ign)
                if not tag:
                    return (False, 'tag not found')

            if category == "account":
                url = f'https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}'

            elif category == "mmr":
                url = f'https://api.henrikdev.xyz/valorant/v2/mmr/ap/{ign}/{tag}'
            
            elif category == "mmr history":
                url = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{ign}/{tag}"
    
    r = requests.get(url, headers=headers)

    if r.status_code in errors.keys():
        return (False, errors[r.status_code])
    
    if r.status_code == 200:
        john = json.loads(r.text)

        if category == 'leaderboard':
            return (True, john)

        if 'error' in john.keys() and john['error'] != None:
            return (False, john['error']['message'])
        
        if 'errors' in john.keys():
            errs = ""
            for error in john['errors']:
                errs += f'{error}, '
            
            if errs != "":
                return (False, errs[:-2])

        if category == 'mmr history':
            if john['name'] == None or john['tag'] == None:
                return (False, 'name/tag error?')
        
        elif category != 'status':
            if john['data']['name'] == None or john['data']['tag'] == None:
                return (False, 'name/tag error?')
        
        return (True, john)

    return (False, 'some error')

def get_tag(ign):
    playerlist = beta_playerclass.PlayerList("playerlistb.csv")
    playerlist.load()

    for player in playerlist.players:
        if ign == player.ign:
            return player.tag
    
    return "False"

def get_file_mmr(puuid):

    if os.path.isfile(f'mmr_history/{puuid}.txt') == False:
        return False
    
    with open(f'mmr_history/{puuid}.txt', 'r') as f:
        for line in f:
            pass

    if line == '\n':
        return False

    #return the latest MMR value in file
    return int(line.split(',')[0])

def initialise_file(puuid):

    f = open(f'mmr_history/{puuid}.txt', "x")
    f.close()

    f = open(f'mmr_history/{puuid}.txt', "w")
    f.write('\n')
    f.close()

def replace_all(string: str, oldValues, newValue):
    for value in oldValues:
        string = string.replace(value, newValue)
    
    return string

def update_database(puuid):

    data = get_data('mmr history', puuid=puuid)
    if not data[0]:
        return data

    data = data[1]['data']

    if os.path.isfile(f'mmr_history/{puuid}.txt') == False:
        if len(data) == 0:
            return (False, 'not enough data')
        else:
            initialise_file(puuid)
    
    # Dates of last update
    date_raw = data[0]['date_raw']
    lines = []

    with open(f'mmr_history/{puuid}.txt', 'r') as f:
        for line in f:
            lines.append(line)
    
    last_file_update = 0 if lines[0] == '\n' else int(lines[0])
    new_list = []

    if last_file_update == 0:
        for i in range(len(data)):
            thedate = replace_all(data[i]['date'], [', ', ' '], '-')
            new_list.append(f"{data[i]['elo']},{thedate}\n")

    elif len(str(last_file_update)) == 13:
        if (len(str(date_raw)) == 10):
            last_file_update = math.floor(last_file_update/1000)
            last_num = last_file_update // 10**0 % 10
            last_num += 1
            last_file_update = math.floor(last_file_update/10) + last_num

        for i in range(len(data)):
            date_raw = data[i]['date_raw']
            if last_file_update < date_raw:
                thedate = replace_all(data[i]['date'], [', ', ' '], '-')
                new_list.append(f"{data[i]['elo']},{thedate}\n")
            else:
                break
    
    else:
        for i in range(len(data)):
            date_raw = data[i]['date_raw']
            if last_file_update < date_raw:
                thedate = replace_all(data[i]['date'], [', ', ' '], '-')
                new_list.append(f"{data[i]['elo']},{thedate}\n")
            else:
                break
    
    if new_list != []:
        lines[0] = f"{data[0]['date_raw']}\n"
        lines += new_list[::-1]

        with open(f'mmr_history/{puuid}.txt', "w") as f:
            f.writelines(lines)
    
    return (True, len(new_list))

def get_elo_list(puuid):
    
    check = update_database(puuid)
    if not check[0]:
        return check

    if not get_file_mmr(puuid):
        return (False, "Player not found")
    
    lines = []
    with open(f'mmr_history/{puuid}.txt', 'r') as f:
        for line in f:
            lines.append(line.strip())

    if len(lines) == 1:
        return (False, "No comp games recorded")
        
    lines.pop(0)
    elolist = ""
    for elem in lines:
        elolist += f"{elem.split(',')[0]}, "

    return (True, elolist[:-2])

def leaderboard(region, length=20):

    if region == 'local':
        playerlist = beta_playerclass.PlayerList('playerlistb.csv')
        playerlist.load()
        players = []

        for player in playerlist.players:
            mmr = get_file_mmr(player.puuid)
            if mmr:
                players.append((player.ign, mmr))
            
        players.sort(key=lambda x:x[1], reverse=True)
        leaderboard = "Player Leaderboard\n"
    
    else:
        data = get_data('leaderboard', region=region)
        if not data[0]:
            return data[1]
        else:
            data = data[1]

        regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}
        players = []
        
        for i in range(length):
            if data[i]['IsAnonymized'] == True:
                players.append(("Anonymous", data[i]['rankedRating']))
            else:
                players.append((data[i]['gameName'], data[i]['rankedRating']))

        leaderboard = f'{regions[region]} Ranked Leaderboard\n'

    for i in range(len(players)):
        rank = i + 1
        leaderboard += (str(rank) + '.').ljust(3) + str(players[i][0]).ljust(16) + str(players[i][1]).rjust(5) + '\n'

    if region == 'local':
        with open("leaderboard.txt", "w") as f:
            f.write(leaderboard)

    return leaderboard

def stats(ign="", tag="", puuid="None"):

    if ign == "" and puuid == "None":
        return (False, False)

    john = get_data('mmr', puuid=puuid, ign=ign, tag=tag)
    if not john[0]:
        return john
    else:
        john = john[1]
    
    data = john['data']['by_season']
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
    
    john = get_data('account', puuid=puuid, ign=ign, tag=tag)
    if not john[0]:
        return john
    else:
        john = john[1]

    card = john['data']['card']['small']
    return (True, [final, card])

def get_banner(ign="", tag="", puuid="None"):

    if ign == "" and puuid == "None":
        return (False, 'no ign or puuid given')

    data = get_data('account', puuid=puuid, ign=ign, tag=tag)
    if not data[0]:
        return data
    else:
        data = data[1]
    
    url = data['data']['card']['large']
    r = requests.get(url, allow_redirects=True)
    open('banner.png', 'wb').write(r.content)
    return (True, True)

def servercheck():
    counter = 0
    report = ""
    regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}

    for elem in regions.keys():
        
        data = get_data('status', region=elem)
        if not data[0]:
            return data[1]
        else:
            data = data[1]

        maintenances = len(data['data']['maintenances'])
        incidents = len(data['data']['incidents'])
        counter += maintenances + incidents

        report += f'{regions[elem]}:\nMaintenances - {maintenances}\nIncidents - {incidents}\n'
        report += f'{regions[elem]}:\n{maintenances} maintenances and {incidents} incidents\n'

    if counter == 0:
        return "no maintenances or incidents reported"
        
    return report

def add_player(ign, tag):

    playerlist = beta_playerclass.PlayerList("playerlistb.csv")
    playerlist.load()

    data = get_data('account', ign=ign, tag=tag)
    if not data[0]:
        return "Account does not exist"
    else:
        data = data[1]

    puuid = data['data']['puuid']
    player = beta_playerclass.Player(ign.lower(), tag.lower(), puuid)
    if playerlist.inList(player):
        return "Account already added"
    
    playerlist.add(player)
    playerlist.save()

    return f'{ign}#{tag} successfully added'

def remove_player(ign):

    playerlist = beta_playerclass.PlayerList("playerlistb.csv")
    playerlist.load()
    tag = get_tag(ign)
    puuid = playerlist.get_puuid_by_ign(ign)
    player = beta_playerclass.Player(ign.lower(), tag, puuid)

    if puuid == "None" or not tag or not playerlist.inList(player):
        return "Player not in list"
        
    playerlist.remove(player)
    playerlist.save()

    return f'{ign}#{tag} has been removed'

def crosshair(code):
    r = get_data("crosshair", crosshair_code=code)
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
    playerlist = beta_playerclass.PlayerList('playerlistb.csv')
    playerlist.load()
    print(leaderboard('local'))