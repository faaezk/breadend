import json
import requests
from flask import Flask
from datetime import datetime

import config
import valorant
import malsearch
import playerclass
import database_updater
from graphs import multigraph

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route('/data/valorant/leaderboard/<region>/<isUpdate>', methods=['GET'])
def leaderboard(region, isUpdate):
    if isUpdate == 'true':
        database_updater.update_all(False, False, False)

    return valorant.leaderboard(region)

@app.route('/data/valorant/stats/<ign>/<tag>', methods=['GET'])
def stats(ign, tag):

    playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerList.load()
    puuid = playerList.get_puuid_by_ign(ign)

    if not puuid and tag != 'emptytag':
        player_data = valorant.get_data("ACCOUNT_BY_NAME", ign=ign, tag=tag)
        puuid = player_data['data']['puuid']
    
    try:
        data = valorant.stats(puuid)
    except Exception as E:
        return json.dumps({"error" : E.message})

    tag = playerList.get_tag_by_ign(ign)
    
    if not data[0]:
        return json.dumps({"error" : "Player not found"})
    
    else:
        stats = data[0]
        fields = []

        for act in stats:
            fields.append({
                "name": act[0],
                "value": act[1]}
            )

        embed = json.dumps({
            "title": "Competitive Statistics",
            "url": "https://youtu.be/kJa2kwoZ2a4?si=K_NtlL62gv2RwhDP",
            "author": f"{ign}#{tag}",
            "thumbnail": data[1],
            "fields": fields
        })

    return embed

@app.route('/data/valorant/graph/<ign_list>', methods=['GET'])
def graph(ign_list):
    playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerList.load()
    ign_list = ign_list.split(',')
    puuid_list = []

    for ign in ign_list:
        puuid = playerList.get_puuid_by_ign(ign.split('#')[0].lower().strip())
        if puuid:
            puuid_list.append(puuid)

    if len(puuid_list) == 0:
        response = {"error" : "No valid players given"}
    
    elif len(puuid_list) == 1:
        with open(f'{config.get("HISTORY_FP")}/{puuid}.txt') as f:
            for line in f:
                pass
            last_game = line.strip()
        
        content = ""

        # If last game is dated, extract day, month and year
        if len(last_game.split(',')) > 1:
            output_format = "%H:%M on %d/%m/%y"
            input_format = "%A-%B-%d-%Y-%I:%M-%p"
            
            date = datetime.strptime(last_game.split(',')[1], input_format)
            content = f'Last game recorded at {date.strftime(output_format)}'
        
        response = json.dumps({
            "content" : content, 
            "filepath" : f'{config.get("GRAPHS_FP")}/{puuid}.png'
        })

    else:
        res = multigraph(puuid_list)
        if res[0] == True:
            response = json.dumps({
                "content" : f"{res[1]}", 
                "filepath" : f'{config.get("MULTI_GRAPH_FP")}'
            })

        else:
            response = json.dumps({"error" : "No valid players given"})

    return response

@app.route('/data/valorant/banner/<username>', methods=['GET'])
def banner(username):

    username = username.lower().split('#')
    if len(username) == 1:
        playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
        playerList.load()
        username.append(playerList.get_tag_by_ign(username[0]))
        if not username[1]:
            return json.dumps({"error" : "Player not in database, provide ign and tag"})

    if valorant.get_banner(ign=username[0], tag=username[1]):
        return json.dumps({"content" : f"Banner for {username[0]}#{username[1]}", "filepath" : config.get("BANNER_FP")})
    else:
        return json.dumps({"error" : "An error occurred while contacting the server."})

@app.route('/data/connected', methods=['GET'])
def chairmen():
    r = requests.get("https://rickies.co/api/chairmen.json", headers={'accept': 'application/json'})
    chairmen = json.loads(r.text)

    keynote = chairmen['keynote_chairman']
    annual = chairmen['annual_chairman']
    return json.dumps({
        "title" : "The Rickies Chairmen",
        "url" : "https://www.relay.fm/connected",
        "fields" : [{"name" : "Keynote Chairman:", "value" : f"{keynote['name']} {keynote['last_name']}"}, 
                    {"name" : "Annual Chairman:", "value" : f"{annual['name']} {annual['last_name']}"}]
    })

@app.route('/data/mal/graph/<category>/<type>/<title>', methods=['GET'])
def mal_graph(category, type, title):
    content = malsearch.score_graph(title, category, type)
    if content == False:
        return json.dumps({"error" : "Server connection error, try again."})
    elif content == None:
        return json.dumps({"error" : f"{category} not found."})
    
    return json.dumps(content)

if __name__ == "__main__":
    app.run(debug=True)