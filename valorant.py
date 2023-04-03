import math
import os
import requests
import json
import playerclass
from PIL import Image
from io import BytesIO
import random
import secret_stuff
from exceptionclass import *

def get_data(endpoint, **kwargs):

    endpoints = {"LEADERBOARD" : "https://api.henrikdev.xyz/valorant/v1/leaderboard/{region}",
                "REGION_STATUS" : "https://api.henrikdev.xyz/valorant/v1/status/{region}",
                "CROSSHAIR" : "https://api.henrikdev.xyz/valorant/v1/crosshair/generate?id={crosshair_code}",
                "ACCOUNT_BY_PUUID" : "https://api.henrikdev.xyz/valorant/v1/by-puuid/account/{puuid}",
                "MMR_BY_PUUID" : "https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/ap/{puuid}",
                "MMR_HISTORY_BY_PUUID" : "https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr-history/ap/{puuid}",
                "ACCOUNT_BY_NAME" : "https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}",
                "MMR_BY_NAME" : "https://api.henrikdev.xyz/valorant/v2/mmr/ap/{ign}/{tag}",
                "MMR_HISTORY_BY_NAME" : "https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{ign}/{tag}"}

    headers = {'accept' : 'application/json', 'Authorization' : secret_stuff.VALORANT_KEY}
    errors = {1 : "Invalid API Key", 2 : "Forbidden endpoint", 3 : "Restricted endpoint", 101 : "No region found for this Player",
            102 : "No matches found, can't get puuid", 103 : "Possible name change detected, can't get puuid. Please play one match, wait 1-2 minutes and try it again",
            104 : "Invalid region", 105 : "Invalid filter", 106 : "Invalid gamemode", 107 : "Invalid map", 108 : "Invalid locale",
            109 : "Missing name", 110 : "Missing tag", 111 : "Player not found in leaderboard", 112 : "Invalid raw type",
            113 : "Invalid match or player id", 114 : "Invalid country code", 115 : "Invalid season", 429 : 'welp', 
            403 : 'Forbidden', 404 : 'User not found', 500 : 'No matches available'}
    
    try:
        url = endpoints[endpoint].format(**kwargs)
    except KeyError:
        raise KeyException

    r = requests.get(url, headers=headers)

    if r.status_code in errors.keys():
        DynamicException.set_message(errors[r.status_code])
        raise DynamicException
    
    if endpoint == 'CROSSHAIR':
        return r
    
    if r.status_code == 200:
        john = json.loads(r.text)

        if endpoint == 'LEADERBOARD':
            return john

        if 'error' in john.keys() and john['error'] != None:
            DynamicException.set_message(john['error']['message'])
            raise DynamicException
        
        if 'errors' in john.keys():
            DynamicException.set_message(' '.join(john['errors']))
            raise DynamicException

        if 'MMR_HISTORY' in endpoint:
            if john['name'] == None or john['tag'] == None:
                raise NoneException
        
        elif endpoint != 'REGION_STATUS':
            if john['data']['name'] == None or john['data']['tag'] == None:
                raise NoneException
        
        return john

    raise UnknownException

def get_tag(ign):
    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()

    for player in playerlist:
        if ign == player.ign:
            return player.tag
    
    return "False"

def get_file_mmr(puuid):

    if os.path.isfile(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt') == False:
        return False
    
    with open(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt', 'r') as f:
        for line in f:
            pass

    if line == '\n':
        return False

    #return the latest MMR value in file
    return int(line.split(',')[0])

def initialise_file(puuid):

    f = open(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt', "x")
    f.close()

    f = open(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt', "w")
    f.write('\n')
    f.close()

def replace_all(string: str, oldValues, newValue):
    for value in oldValues:
        string = string.replace(value, newValue)
    
    return string

def update_database(puuid):

    try: 
        data = get_data('MMR_HISTORY_BY_PUUID', puuid=puuid)
    except Exception as E:
        raise E

    data = data['data']

    if not os.path.isfile(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt'):
        if len(data) == 0:
            raise NoneException
        else:
            initialise_file(puuid)
    
    # Dates of last update
    date_raw = data[0]['date_raw']
    lines = []

    with open(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt', 'r') as f:
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

        with open(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt', "w") as f:
            f.writelines(lines)
    
    return len(new_list)

def get_elo_list(puuid):
    
    try: 
        update_database(puuid)
    except Exception as E:
        raise E

    if not get_file_mmr(puuid):
        return MissingException
    
    lines = []
    with open(f'{secret_stuff.DATABASE_PATH}/{puuid}.txt', 'r') as f:
        for line in f:
            lines.append(line.strip())

    if len(lines) == 1:
        raise NoneException
        
    lines.pop(0)
    elolist = ""
    for elem in lines:
        elolist += f"{elem.split(',')[0]}, "

    return elolist[:-2]

def leaderboard(region, length=20):

    if region == 'local':
        playerlist = playerclass.PlayerList('playerlist.csv')
        playerlist.load()
        players = []

        for player in playerlist:
            mmr = get_file_mmr(player.puuid)
            if mmr:
                players.append((player.ign, mmr))
            
        players.sort(key=lambda x:x[1], reverse=True)
        leaderboard = "Player Leaderboard\n"
    
    else:
        try:
            data = get_data('LEADERBOARD', region=region)
        except Exception as E:
            raise E

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
        with open("stuff/leaderboard.txt", "w") as f:
            f.write(leaderboard)

    return leaderboard

def stats(puuid):

    try:
        john = get_data('MMR_BY_PUUID', puuid=puuid)
    except Exception as E:
        raise E
    
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
    
    try:
        john = get_data('ACCOUNT_BY_PUUID', puuid=puuid)
    except Exception as E:
        raise E

    card = john['data']['card']['small']
    return [final, card]

def get_banner(puuid):

    try:
        data = get_data('ACCOUNT_BY_PUUID', puuid=puuid)
    except Exception as E:
        raise E
    
    url = data['data']['card']['large']
    r = requests.get(url, allow_redirects=True)
    open('stuff/banner.png', 'wb').write(r.content)
    
    return True

def servercheck():
    counter = 0
    report = ""
    regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}

    for elem in regions.keys():
        
        try:
            data = get_data('REGION_STATUS', region=elem)
        except Exception as E:
            report += f'{regions[elem]}:\n Error: {E.message}\n'

        maintenances = len(data['data']['maintenances'])
        incidents = len(data['data']['incidents'])
        counter += maintenances + incidents

        report += f'{regions[elem]}:\nMaintenances - {maintenances}\nIncidents - {incidents}\n'
        report += f'{regions[elem]}:\n{maintenances} maintenances and {incidents} incidents\n'

    if counter == 0:
        return "no maintenances or incidents reported"
        
    return report

def add_player(ign, tag):

    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()

    try:
        data = get_data('ACCOUNT_BY_NAME', ign=ign, tag=tag)
    except Exception as E:
        return E.message

    puuid = data['data']['puuid']
    player = playerclass.Player(ign.lower(), tag.lower(), puuid)
    if playerlist.inList(player):
        return "Account already added"
    
    playerlist.add(player)
    playerlist.save()

    return f'{ign}#{tag} successfully added'

def remove_player(ign):

    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()
    tag = get_tag(ign)
    puuid = playerlist.get_puuid_by_ign(ign)
    player = playerclass.Player(ign.lower(), tag, puuid)

    if puuid == "None" or not tag or not playerlist.inList(player):
        return "Player not in list"
        
    playerlist.remove(player)
    playerlist.save()

    return f'{ign}#{tag} has been removed'

def crosshair(code):
    try:
        r = get_data("CROSSHAIR", crosshair_code=code)
    except Exception as E:
        raise E
    
    img = Image.open(BytesIO(r.content))
    img = img.save("stuff/crosshair.png")

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

    try:
        crosshair(code)
    except Exception as E:
        return E.message

    return (name, code)

def update_playerlist():
    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()
    updates = 0
    for player in playerlist:

        try:
            response = get_data("ACCOUNT_BY_PUUID", puuid=player.puuid)
        except Exception as E:
            raise E

        true_ign = response['data']['name'].lower()
        true_tag = response['data']['name'].lower()

        if (player.ign != true_ign) or (player.tag != true_tag):
            updates += 1

        player.ign = true_ign
        player.tag = true_tag

    playerlist.save()

    return updates
