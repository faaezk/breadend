import os, json, requests
from datetime import datetime
from flask import Flask, abort, jsonify, send_file, url_for

import config, graphs, valorant, malsearch, playerclass, database_updater

app = Flask(__name__)

@app.errorhandler(400)
def bad_request_error(error):
    response = jsonify({"error": "Bad Request", "message": error.description})
    response.status_code = 400
    return response

@app.errorhandler(500)
def internal_error(error):
    response = jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"})
    response.status_code = 500
    return response

@app.route('/')
def index():
    return "Hello"

@app.route('/image/<img_type>/<filename>', methods=['GET'])
def get_image(img_type, filename):
    
    image_path = f'{config.get(img_type)}/{filename}'
    if not os.path.isfile(image_path):
        abort(400, "File not found")

    return send_file(image_path, mimetype='image/png')

@app.route('/valorant/leaderboard/<region>', defaults={'toUpdate': 'false'}, methods=['GET'])
@app.route('/valorant/leaderboard/<region>/<toUpdate>', methods=['GET'])
def leaderboard(region, toUpdate):
    if toUpdate == 'true' and region == 'local':
        database_updater.update_all(False, False)

    res = valorant.leaderboard(region)
    if "error" in res.keys():
        abort(400, res['error'])
    else:
        return jsonify(res)

@app.route('/valorant/stats/<ign>', defaults={'tag': ''}, methods=['GET'])
@app.route('/valorant/stats/<ign>/<tag>', methods=['GET'])
def stats(ign, tag):
    if tag == '':
        playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
        playerList.load()
        tag = playerList.get_tag_by_ign(ign)
        puuid = playerList.get_puuid_by_ign(ign)
        
        if not ign or not tag:
            abort(400, "Player not in database, provide ign and tag")
    else:
        try:
            player_data = valorant.get_data("ACCOUNT_BY_NAME", ign=ign, tag=tag)
        except Exception as E:
            abort(400, str(E))
        puuid = player_data['data']['puuid']
    
    try:
        data = valorant.stats(puuid)
    except Exception as E:
        abort(400, str(E))
    
    if not data[0]:
        abort(400, "Player not found")
    else:
        stats = data[0]
        acts = [{"name": act[0], "value": act[1]} for act in stats]
        return jsonify({
            "author": f"{ign}#{tag}",
            "thumbnail": data[1],
            "acts": acts
        })

@app.route('/valorant/banner/<ign>', defaults={'tag': ''}, methods=['GET'])
@app.route('/valorant/banner/<ign>/<tag>', methods=['GET'])
def banner(ign, tag):
    if tag == '':
        playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
        playerList.load()
        tag = playerList.get_tag_by_ign(ign)
        if not tag:
            abort(400, "Player not in database, provide ign and tag")

    if valorant.get_banner(ign, tag):
        return jsonify({"content" : f'Banner for {ign}#{tag}', 
                        "file" : url_for('get_image', type='RES', filename='banner.png', _external=True)})
    else:
        abort(400, "An error occurred while contacting the server.")

@app.route('/valorant/graph/<ign_list>', defaults={'acts': 'false'}, methods=['GET'])
@app.route('/valorant/graph/<ign_list>/<acts>', methods=['GET'])
def graph(ign_list, acts):
    playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerList.load()
    ign_list = ign_list.split(',')
    puuid_list = []

    for ign in ign_list:
        puuid = playerList.get_puuid_by_ign(ign.split('#')[0].lower().strip())
        if puuid:
            puuid_list.append(puuid)

    if len(puuid_list) == 0:
        abort(400, "No valid players given")
    
    elif len(puuid_list) == 1:
        puuid = puuid_list[0]
        with open(f"{config.get('MMR_HISTORY')}/{puuid}.txt") as f:
            for line in f:
                pass
            last_game = line.strip()
        
        if acts == 'true':
            graphs.graph(puuid, acts=True)
        else:
            graphs.graph(puuid, acts=False)
        
        # If last game is dated, extract day, month and year
        content = ""
        if len(last_game.split(',')) > 1:
            output_format = "%H:%M on %d/%m/%y"
            input_format = "%A-%B-%d-%Y-%I:%M-%p"
            
            date = datetime.strptime(last_game.split(',')[1], input_format)
            content = f'Last game recorded at {date.strftime(output_format)}'
        
        response = jsonify({
            "content" : content, 
            "file" : url_for('get_image', type='MMR_GRAPH', filename=f'{puuid}.png', _external=True)
        })

    else:
        res = graphs.multigraph(puuid_list)
        if res[0] == True:
            response = jsonify({
                "content" : f"{res[1]}", 
                "file" : url_for('get_image', type='RES', filename='multigraph.png', _external=True)
            })

        else:
            abort(400, "No valid players given")

    return response

@app.route('/mal/info/anime/<title>', defaults={'anime_type': 'tv'}, methods=['GET'])
@app.route('/mal/info/anime/<anime_type>/<title>', methods=['GET'])
def anime_stats(anime_type, title):
    anime = malsearch.anime_search(anime_type, title)
    if anime is False:
        abort(400, "Server connection error, try again.")
    elif anime is None:
        abort(400, "Anime not found.")
    
    return jsonify(anime)

@app.route('/mal/info/manga/<title>', methods=['GET'])
def manga_stats(title):
    manga = malsearch.manga_search(title)
    if manga is False:
        abort(400, "Server connection error, try again.")
    elif manga is None:
        abort(400, "Manga not found.")

    return jsonify(manga)

@app.route('/mal/info/character/<name>', methods=['GET'])
def character_stats(name):
    character = malsearch.character_search(name)
    if character is False:
        abort(400, "Server connection error, try again.")
    elif character is None:
        abort(400, "Character not found.")

    return jsonify(character)

@app.route('/mal/graph/<category>/<title>', defaults={'graph_type': 'tv'}, methods=['GET'])
@app.route('/mal/graph/<category>/<graph_type>/<title>', methods=['GET'])
def mal_graph(category, graph_type, title):
    content = malsearch.score_graph(title, category, graph_type)
    if content is False:
        abort(400, "Server connection error, try again.")
    elif content is None:
        abort(400, f"{category} not found.")
    
    content['file'] = url_for('get_image', type='RES', filename='mal_graph.png', _external=True)
    return jsonify(content)

@app.route('/other/connected', methods=['GET'])
def chairmen():
    try:
        r = requests.get("https://rickies.co/api/chairmen.json", headers={'accept': 'application/json'}, timeout=10)
        r.raise_for_status()
        chairmen = r.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        abort(400, f"Failed to fetch chairmen data: {str(e)}")

    keynote = chairmen['keynote_chairman']
    annual = chairmen['annual_chairman']
    return jsonify({
        "title" : "The Rickies Chairmen",
        "url" : "https://www.relay.fm/connected",
        "image_url" : "https://relayfm.s3.amazonaws.com/uploads/broadcast/image_3x/5/connected_artwork_0ecdaa3e-7019-4a34-86f7-f82d6a997144.png",
        "chairmen" : [{"name" : "Keynote Chairman:", "value" : f"{keynote['name']} {keynote['last_name']}"}, 
                    {"name" : "Annual Chairman:", "value" : f"{annual['name']} {annual['last_name']}"}]
    })

if __name__ == "__main__":
   app.run(debug=True)

# def create_app():
#    return app