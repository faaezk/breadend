import json
from flask import Flask
from datetime import datetime

import config
import valorant
import playerclass

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route('/data/valorant/leaderboard/<region>/<isUpdate>', methods=['GET'])
def leaderboard(region, isUpdate):

    if isUpdate == 'true':
        # update with mmr_history_updater.update_all(False, printer=False)
        pass

    return valorant.leaderboard(region)

@app.route('/data/valorant/stats/<ign>/<int:tag>', methods=['GET'])
def stats(ign, tag):

    playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerList.load()
    puuid = playerList.get_puuid_by_ign(ign)

    if puuid == "None" and tag != 'emptytag':
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

@app.route('/data/valorant/graph/<ign>', methods=['GET'])
def graph(ign):
    playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerList.load()
    puuid = playerList.get_puuid_by_ign(ign)

    if puuid == None:
        return json.dumps({"error" : "Player not in database"})

    with open(f'{config.get("HISTORY_FP")}/{puuid}.txt') as f:
        for line in f:
            pass
        last_game = line.strip()
    
    content = ""

    # If last game is dated, extract day, month and year
    if len(last_game.split(',')) > 1:
        output_format = "%d/%m/%y"
        input_format = "%A-%B-%d-%Y-%I:%M-%p"
        
        date = datetime.strptime(last_game.split(',')[1], input_format)
        content = f'Last game played on {date.strftime(output_format)}'
    
    response = json.dumps({
        "content" : content, 
        "filepath" : f'{config.get("GRAPHS_FP")}/{puuid}.png'
    })
    
    return response



if __name__ == "__main__":
    app.run(debug=True)