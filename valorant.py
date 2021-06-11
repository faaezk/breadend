import requests
import json

players = [("silentwhispers", "0000"), 
    ("Fakinator", "4269"), 
    ("faqinator", "7895"), 
    ("8888", "nadi"), 
    ("dilka30003", "0000"),
    ("slumonaire", "oce"),
    ("KATCHAMPION", "oce"), 
    ("imabandwagon", "oce"), 
    ("giroud", "8383"), 
    ("oshaoshawott", "oce"), 
    ("YoVivels", "1830"), 
    ("therealrobdez", "3333"),
    ("bento2", "box"), 
    ("hoben222", "9327"), 
    ("jokii", "oce")]

def get_player_data(username, tagline):
    url = "https://api.henrikdev.xyz/valorant/v1/mmr/ap/{}/{}".format(username, tagline)
    r = requests.get(url)
    return r.text

def get_elos():
    
    bohn = []

    for i in range(0, len(players)):
        if players[i][0] == "8888":
            bohn.append((69, players[i][0]))
            
        else:
            data = get_player_data(players[i][0], players[i][1])
            john = json.loads(data)
            bohn.append((john['data']['elo'], players[i][0]))

    return sorted(bohn, reverse=True)

def elo_leaderboard():

    bohn = get_elos()
    leaderboard = ""
    
    for i in range(0, len(bohn)):

        user = bohn[i][1]
        elo = bohn[i][0]
        rank = i + 1
        leaderboard += "{}. {} {}\n".format(rank, user, elo)

    return leaderboard