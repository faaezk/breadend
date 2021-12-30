import os
import requests
import json
import playerclass

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
    r = requests.get(url)

    if str(r) == "<Response [204]>" or str(r) == "<Response [504]>":
        return False

    john = json.loads(r.text)

    if 'status' in john:
        if john['status'] == '429':
            return "welp"
        
        elif john['status'] == '404':
            return "User not found"
        
        elif john['status'] == '500':
            return "No matches available"
        
        elif john['status'] != '200':
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

    return john

def get_file_mmr(ign):

    file_path = f'/home/ubuntu/discord_bot/elo_history/{ign}.txt'

    if os.path.isfile(file_path) == False:
        return False

    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()

    if lines[-1] == '\n':
        return False

    #return the latest MMR value in file
    return int(lines[-1])

def initialise_file(ign):

    f = open(f'/home/ubuntu/discord_bot/elo_history/{ign}.txt', "x")
    f.close()

    f = open(f'/home/ubuntu/discord_bot/elo_history/{ign}.txt', "w")
    f.writelines('\n')
    f.close()

def update_database(ign, tag=""):

    if tag == "":
        tag = get_tag(ign)
        if not tag:
            return False
    
    player_data = get_mmr_history(ign, tag)

    if type(player_data) != dict:
        return False

    player_file_path = f'/home/ubuntu/discord_bot/elo_history/{ign}.txt'

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
    i = 0

    if last_file_update == 0:
        for i in range(0, len(player_data['data'])):
            new_list.append(player_data['data'][i]['elo'])

    elif len(str(last_file_update)) == 13:

        for i in range(0, len(player_data['data'])):

            date_raw = player_data['data'][i]['date_raw']

            if (len(str(date_raw)) == 10):
                last_file_update = int(str(last_file_update)[-3])

            if last_file_update < date_raw:
                new_list.append(player_data['data'][i]['elo'])
            else:
                break
    
    else:
        for i in range(0, len(player_data['data'])):

            date_raw = player_data['data'][i]['date_raw']

            if last_file_update < date_raw:
                new_list.append(player_data['data'][i]['elo'])
            else:
                break
    
    new_list = new_list[::-1]

    player_file = open(player_file_path, 'a')
    
    for elem in range(0, len(new_list)):
        player_file.writelines(str(new_list[elem]) + '\n')

    player_file.close()

    #update timestamp in file
    with open(player_file_path) as f:
        lines = f.readlines()
    
    lines[0] = str(player_data["data"][0]["date_raw"]) + '\n'

    with open(player_file_path, "w") as f:
        f.writelines(lines)
    
    return len(new_list)

def get_elo_list(ign):
    
    tag = get_tag(ign)
    if not tag:
        return "Player not found"

    update_database(ign, tag)

    if not get_file_mmr(ign):
        return "Player not found"
    
    file1 = open(f'/home/ubuntu/discord_bot/elo_history/{ign}.txt', 'r')

    lines = [x.strip() for x in file1.readlines()]

    if len(lines) == 1:
        return "No comp games recorded"
        
    lines.pop(0)
    
    elolist = ""

    for elem in lines:
        elolist += elem + ", "

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
    r = requests.get(url)

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

    if data['status'] == '404' or data['status'] == '500':
        return "Player not found, check syntax: (ign#tag)"
    
    url = data['data']['card']['large']
    r = requests.get(url, allow_redirects=True)

    open('banner.png', 'wb').write(r.content)

    return True

def account_check(ign, tag):

    url = f'https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}'

    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return False

    data = json.loads(r.text)

    if 'status' in data:
        if data['status'] == '404':
            return False
    
    if 'statusCode' in data:
        if data['statusCode'] != 404:
            return False

    return True

def servercheck():

    counter = 0
    report = ""
    regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}

    for elem in regions.keys():
        
        url = f'https://api.henrikdev.xyz/valorant/v1/status/{elem}'

        r = requests.get(url)

        if str(r) == "<Response [204]>":
            break

        john = json.loads(r.text)

        if 'status' in john:
            if john['status'] != '200':
                break
        
        if 'statusCode' in john:
            if john['statusCode'] != 200:
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

if __name__ == '__main__':
    print(update_database('fakinator'))