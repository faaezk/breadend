import requests
import json

url = f"https://api.henrikdev.xyz/valorant/v1/leaderboard/kr"
r = requests.get(url)

data = json.loads(r.text)
players = []
length = 20
    
for i in range(length):
        players.append([data[i]['gameName'], data[i]['rankedRating']])
        ign = data[i]['gameName']
        print(ign + "  " + str(len(ign)))

rleaderboard = ""
    
for i in range(0, len(players)):

    elo = players[i][1]
    user = players[i][0]
    rank = i + 1
    rleaderboard += str(str(rank) + '.').ljust(3) + str(user).ljust(20) + str(elo).rjust(5) + '\n'

