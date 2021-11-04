from datetime import datetime
import requests
import json
import os
import playerclass

def get_tag(username):
    
    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()

    tagline = "Player not found."
    for player in playerlist.players:
        if player.ign == username:
            tagline = player.tag
            break
    
    return tagline

def get_elo_history(username, tagline):
    
    url = "https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{}/{}".format(username, tagline)
    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return False

    john = json.loads(r.text)

    if john['status'] == '404' or john['status'] == '500':
        return False
    
    if john['status'] == '429':
        return "welp"

    return john

def get_elo_from_file(username):

    file_path = '/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username)

    if os.path.isfile(file_path) == False:
        return False

    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()

    return int(lines[-1])

def initialise_file(username):

    f = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), "x")
    f.close()

    f = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), "w")
    f.writelines(str(0) + '\n')
    f.close()

    return

def update_elo_history(username, tagline):

    player_data = get_elo_history(username, tagline)

    if player_data == False:
        return -1
    
    if player_data == "welp":
        return "welp"
    
    player_file_path = f'/home/ubuntu/discord_bot/elo_history/{username}.txt'

    if os.path.isfile(player_file_path) == False:
        initialise_file(username)

    # Dates of last update
    date_raw = player_data["data"][0]["date_raw"]
    player_file = open(player_file_path, 'r')
    last_file_update = int(player_file.readline())
    player_file.close()

    new_elo_list = []
    i = 0

    if last_file_update == 0:
        for i in range(0, len(player_data['data'])):
            new_elo_list.append(player_data['data'][i]['elo'])

    else:
        for i in range(0, len(player_data['data'])):

            date_raw = player_data['data'][i]['date_raw']

            if last_file_update < date_raw:
                new_elo_list.append(player_data['data'][i]['elo'])
            else:
                break
    
    correctly_sorted_new_elo_list = new_elo_list[::-1]

    player_file = open(player_file_path, 'a')
    
    for elem in range(0, len(correctly_sorted_new_elo_list)):
        player_file.writelines(str(correctly_sorted_new_elo_list[elem]) + '\n')

    player_file.close()

    #update timestamp in file
    with open(player_file_path) as f:
        lines = f.readlines()
    
    lines[0] = str(player_data["data"][0]["date_raw"]) + '\n'

    with open(player_file_path, "w") as f:
        f.writelines(lines)   
    
    return len(correctly_sorted_new_elo_list)

def get_elolist(username):
    
    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()

    tagline = ""
    for player in playerlist.players:
        if player.ign == username:
            tagline = player.tag
            break
    
    update_elo_history(username, tagline)

    if os.path.isfile('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username)) == False:
        return "Player not found or hasn't played any comp games recently"
    
    file1 = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), 'r')

    lines = [x.strip() for x in file1.readlines()]
    if len(lines) == 1:
        return None
    lines.pop(0)
    
    elolist = ""

    for elem in lines:
        elolist += elem + ", "

    return elolist[:-2]

def elo_leaderboard():

    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()
    
    bohn = []

    for player in playerlist.players:

        file_elo = get_elo_from_file(player.ign)

        if type(file_elo) == int:
            bohn.append((file_elo, player.ign))

    bohn = sorted(bohn, reverse=True)
    leaderboard = "Player Leaderboard\n"

    for i in range(0, len(bohn)):

        user = bohn[i][1]
        elo = bohn[i][0]
        rank = i + 1
        leaderboard += str(str(rank) + '.').ljust(3) + str(user).ljust(16) + str(elo).rjust(5) + '\n'

    f = open("leaderboard.txt", "w")
    f.write(leaderboard)
    f.close()

    return leaderboard

def region_leaderboard(region):

    url = f"https://api.henrikdev.xyz/valorant/v1/leaderboard/{region}"
    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return False

    data = json.loads(r.text)
    players = []
    length = 20
    
    for i in range(length):
        if data[i]['IsAnonymized'] == True:
            players.append(["Anonymous", data[i]['rankedRating']])
        else:
            players.append([data[i]['gameName'], data[i]['rankedRating']])

    rleaderboard = ""
    
    for i in range(0, len(players)):

        elo = players[i][1]
        user = players[i][0]
        rank = i + 1
        rleaderboard += str(str(rank) + '.').ljust(3) + str(user).ljust(20) + str(elo).rjust(5) + '\n'

    return rleaderboard

def stats(ign, tag):

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
    
    return final

#Don't remove as this is how the leaderboard is being refreshed
if __name__ == "__main__":
    leaderboard = elo_leaderboard()

    f = open("leaderboard.txt", "w")
    f.write(leaderboard)
    f.close()
    #print("leaderboard updated")