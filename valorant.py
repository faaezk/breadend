import os
import requests
import json
import playerclass
from PIL import Image
from io import BytesIO
import random
import configparser

def get_data(category, ign="", tag="", region="", crosshair_code=""):

    key = get_key()
    headers = {'accept' : 'application/json', 'Authorization' : key}
    errors = {429 : 'welp', 403 : 'Forbidden', 404 : 'User not found', 500 : 'No matches available'}

    if region != "":
        if category == "leaderboard":
            url = f"https://api.henrikdev.xyz/valorant/v1/leaderboard/{region}"
        
        if category == "status":
            url = f'https://api.henrikdev.xyz/valorant/v1/status/{region}'

    elif category == "crosshair":
        url = f"https://api.henrikdev.xyz/valorant/v1/crosshair/generate?id={crosshair_code}"
        return requests.get(url, headers=headers)

    else:
        if ign == "":
            return(False, False)

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

        if ign != "":
            if john['name'] == None or john['tag'] == None or ('error' in john.keys()):
                return (False, 'name/tag error?')
        
        return (True, john)

    return (False, 'some error')

def get_key():
    c = configparser.ConfigParser()
    c.read('config.ini')

    return c['henrik']['key']

def get_tag(ign):
    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()

    for player in playerlist.players:
        if ign == player.ign:
            return player.tag
    
    return False

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

    player_data = get_data('mmr history', ign=ign, tag=tag)
    if not player_data[0]:
        return player_data
    else:
        player_data = player_data[1]

    player_file_path = f'elo_history/{ign}.txt'

    if os.path.isfile(player_file_path) == False:
        if len(player_data['data']) == 0:
            return (False, 'not enough data')
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

        for i in range(len(player_data['data'])):
            thedate = player_data['data'][i]['date'].replace(',', '-').replace(' ', '-').replace('--', '-')
            new_list.append(str(player_data['data'][i]['elo']) + ',' + thedate)


    elif len(str(last_file_update)) == 13:
        
        if (len(str(date_raw)) == 10):
            last_file_update = int(str(last_file_update)[:-3])
            last_num = int(str(last_file_update)[-1])
            last_num += 1
            last_file_update = int(str(last_file_update)[:-1] + str(last_num))

        for i in range(len(player_data['data'])):

            date_raw = player_data['data'][i]['date_raw']

            if last_file_update < date_raw:
                thedate = player_data['data'][i]['date'].replace(',', '-').replace(' ', '-').replace('--', '-')
                new_list.append(str(player_data['data'][i]['elo']) + ',' + thedate)

            else:
                break
    
    else:
        for i in range(len(player_data['data'])):

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
        
        for elem in range(len(new_list)):
            player_file.writelines(str(new_list[elem]) + '\n')

        player_file.close()
    
    return (True, len(new_list))

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

    for i in range(len(players)):

        ign = players[i][0]
        mmr = players[i][1]
        rank = i + 1
        leaderboard += (str(rank) + '.').ljust(3) + str(ign).ljust(16) + str(mmr).rjust(5) + '\n'

    f = open("leaderboard.txt", "w")
    f.write(leaderboard)
    f.close()

    return leaderboard

def region_leaderboard(region, length=20):

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

        ign = players[i][0]
        mmr = players[i][1]
        rank = i + 1
        leaderboard += (str(rank) + '.').ljust(3) + str(ign).ljust(16) + str(mmr).rjust(5) + '\n'

    return leaderboard    

def stats(ign, tag=""):

    john = get_data('mmr', ign=ign, tag=tag)
    if not john[0]:
        return john[1]
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
    
    john = get_data('account', ign=ign, tag=tag)
    if not john[0]:
        return john[1]
    else:
        john = john[1]

    card = john['data']['card']['small']

    return [final, card]

def get_banner(ign, tag):

    data = get_data('account', ign=ign, tag=tag)
    if not data[0]:
        return data[1]
    else:
        data = data[1]
    
    url = data['data']['card']['large']
    r = requests.get(url, allow_redirects=True)

    open('banner.png', 'wb').write(r.content)

    return True

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

    playerlist = playerclass.PlayerList("playerlist.csv")
    playerlist.load()

    if not get_data('account', ign=ign, tag=tag)[0]:
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
    print(servercheck())