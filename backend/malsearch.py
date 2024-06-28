import json
import requests
import matplotlib.pyplot as plt

import config

def trim(text, limit):
    if len(text) > limit:
        text = text[0:limit]
        text += "...\nMore at MyAnimeList (link in title)"
    return text

def api_request(query, category, type="", stats=False):

    session = requests.Session()
    if type == "":
        r = session.get(f'https://api.jikan.moe/v4/{category}?q={query}&page=1&limit=1')
    else:
        r = session.get(f'https://api.jikan.moe/v4/{category}?q={query}&type={type}&page=1&limit=1')

    if r.status_code != 200:
        return False

    res = json.loads(r.text)
    if not ('data' in res.keys() and len(res['data']) > 0):
        return None
    
    id = res['data'][0]['mal_id']
    if stats:
        title = res['data'][0]['title']
        url = res['data'][0]['url']
        typer = res['data'][0]['type']

    if stats:
        r = session.get(f'https://api.jikan.moe/v4/{category}/{id}/statistics')
    else:
        r = session.get(f'https://api.jikan.moe/v4/{category}/{id}/full')

    if r.status_code != 200:
        return False

    res = json.loads(r.text)
    if not ('data' in res.keys()):
        return None

    if stats:
        res['data']['title'] = title
        res['data']['url'] = url
        res['data']['type'] = typer

    return res['data']

def anime_search(title, type):

    anime = api_request(title, "anime", type)
    if not anime:
        return None
    
    data = {"Airing_Dates" : anime['aired']['string'], "source" : anime['source'], 
            "type" : anime['type'], "score" : anime['score'], "url" : anime['url'],
            "eng_title" : anime['title_english'], "jap_title" : anime['title_japanese']}
    
    data['ep_count'] = '?' if not anime['episodes'] else str(anime['episodes'])
    data['synopsis'] = trim(anime['synopsis'], 980)

    data['opening_themes'] = ""
    if 'openings' in anime['theme'].keys():
        for theme in anime['theme']['openings']:
            if len(data['opening_themes']) > 989:
                data['opening_themes'] = data['opening_themes'][:-(len(last) + 1)]
                data['opening_themes'] += "more at MyAnimeList (link in title)"
                break
            data['opening_themes'] += theme + '\n'
            last = theme

    data['ending_themes'] = ""
    if 'endings' in anime['theme'].keys():
        for theme in anime['theme']['endings']:
            if len(data['ending_themes']) > 989:
                data['ending_themes'] = data['ending_themes'][:-(len(last) + 1)]
                data['ending_themes'] += "more at MyAnimeList (link in title)"
                break
            data['ending_themes'] += theme + '\n'
            last = theme

    data['sequel'] = ""
    for related in anime['relations']:
        if related['relation'] == 'Sequel':
            sequel_list = related['entry']
            if len(sequel_list) == 1:
                data['sequel'] = sequel_list[0]['name'] + '\n'
            else:
                for i in range(sequel_list):
                    data['sequel'] += str(i + 1) + '. ' + sequel_list[i]['name'] + '\n'

            data['sequel'] = data['sequel'][:-1]
            break

    data['genres'] = ""
    for genre in anime['genres']:
        data['genres'] += genre['name'] + ', '
    data['genres'] = data['genres'][:-2]

    data['studios'] = ""
    for studio in anime['studios']:
        data['studios'] += studio['name'] + ', '
    data['studios'] = data['studios'][:-2]

    data['licensors'] = ""
    for licensor in anime['licensors']:
        data['licensors'] += licensor['name'] + ', '
    data['licensors'] = data['licensors'][:-2]

    data['image_url'] = ""
    if 'jpg' in anime['images'].keys():
        data['image_url'] = anime['images']['jpg']['image_url']

    for key in data.keys():
        if data[key] == "":
            data[key] = "None"
    
    return data

def manga_search(title):

    manga = api_request(title, "manga")
    if not manga:
        return None
    
    data = {"publishing" : manga['published']['string'], "score" : manga['score'], 
            "type" : manga['type'], "rank" : manga['rank'], "url" : manga['url'],
            "eng_title" : manga['title_english'], "jap_title" : manga['title_japanese']}

    data['vol_count'] = '?' if not manga['volumes'] else str(manga['volumes'])
    data['chap_count'] = '?' if not manga['chapters'] else str(manga['chapters'])
    data['synopsis'] = trim(manga['synopsis'], 980)

    data['genres'] = ""
    for genre in manga['genres']:
        data['genres'] += genre['name'] + ', '
    data['genres'] = data['genres'][:-2]

    data['authors'] = ""
    for author in manga['authors']:
        data['authors'] += author['name'] + '\n'
    data['authors'] = data['authors'][:-1]

    data['serializations'] = ""
    for serializations in manga['serializations']:
        data['serializations'] += serializations['name'] + ', '
    data['serializations'] = data['serializations'][:-2]

    data['image_url'] = ""
    if 'jpg' in manga['images'].keys():
        data['image_url'] = manga['images']['jpg']['image_url']

    for key in data.keys():
        if data[key] == "":
            data[key] = "None"
    
    return data

def character_search(name):
    
    character = api_request(name, "characters")
    if not character:
        return None

    data = {"url" : character['url'], "name" : character['name'],
            "favorites" : character["favorites"]}

    data['description'] = trim(character['about'], 980)

    data['anime'] = ""
    for show in character['anime']:
        if len(data['anime']) > 989:
            data['anime'] = data['anime'][:-(len(last))]
            data['anime'] += "more at MyAnimeList (link in title)"
            break
        
        last = show['anime']['title'] + '\n'
        data['anime'] += last

    data['manga'] = ""
    for book in character['manga']:
        if len(data['manga']) > 989:
            data['manga'] = data['manga'][:-(len(last))]
            data['manga'] += "more at MyAnimeList (link in title)"
            break

        last = book['manga']['title'] + '\n'
        data['manga'] += last

    data['voice_actors'] = ""
    for va in character['voices']:

        if len(data['voice_actors']) > 989:
            data['voice_actors'] = data['voice_actors'][:-(len(last))]
            data['voice_actors'] += "More at MyAnimeList (link in title)"
            break
        
        last = va['language'] + ': ' + va['person']['name'] + '\n'
        data['voice_actors'] += last

    data['image_url'] = ""
    if 'jpg' in character['images'].keys():
        data['image_url'] = character['images']['jpg']['image_url']

    for key in data.keys():
        if data[key] == "":
            data[key] = "None"

    return data

def generate_graph(x, y, title):
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel('Scores')
    plt.ylabel('Votes')
    
    # Create names on the x axis
    plt.xticks(x)
    plt.yticks()

    for i in range(len(x)):
        plt.text(i, y[i], str(y[i]), ha = 'center')

    plt.savefig(config.get("MAL_STATS_FP"), bbox_inches='tight')
    plt.clf()

def score_graph(title, category, type=""):

    res = api_request(title, category, type, stats=True)
    if not res:
        return None
    
    data = {"completed" : res["completed"], "on_hold" : res["on_hold"],
        "dropped" : res["dropped"], "total" : res["total"], "title" : res['title'], "url" : res['url']}
    
    if category == "manga":
        data["reading"] = res["reading"]
        data["plan_to_read"] = res["plan_to_read"]
    else:
        data["watching"] = res["watching"]
        data["plan_to_watch"] = res["plan_to_watch"]

    x = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    y = [score['votes'] for score in res['scores']]

    generate_graph(x, y, f'{res['title']} ({res['type']}) Vote distribution')
    return data