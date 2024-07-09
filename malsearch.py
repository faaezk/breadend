import json
import requests
import matplotlib.pyplot as plt

import config

def trim(text, limit):
    if len(text) > limit:
        text = text[0:limit]
        text += "...\nMore at MyAnimeList (link in title)"
    return text

def api_request(query, category, type="null", stats=False):

    session = requests.Session()
    if type == "null":
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

def anime_search(type, title):

    anime = api_request(title, "anime", type)
    if not anime:
        return None
    
    data = {"Airing_Dates" : anime['aired']['string'], "source" : anime['source'], 
            "type" : anime['type'], "score" : anime['score'], "url" : anime['url'],
            "eng_title" : anime['title_english'], "jap_title" : anime['title_japanese']}
    
    data['ep_count'] = '?' if not anime['episodes'] else str(anime['episodes'])
    data['synopsis'] = trim(anime['synopsis'], 980)

    data['opening_themes'] = []
    if 'openings' in anime['theme'].keys():
        for op in anime['theme']['openings']:
            data['opening_themes'].append(op)

    data['ending_themes'] = []
    if 'endings' in anime['theme'].keys():
        for ed in anime['theme']['endings']:
            data['ending_themes'].append(ed)

    data['sequel'] = []
    for related in anime['relations']:
        if related['relation'] == 'Sequel':
            for sequel in related['entry']:
                data['sequel'].append(sequel['name'])

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

    data['anime'] = []
    for show in character['anime']:
        data['anime'].append(show['anime']['title'])

    data['manga'] = []
    for book in character['manga']:
        data['manga'].append(book['manga']['title'])

    data['voice_actors'] = []
    for va in character['voices']:
        data['voice_actors'].append((va['person']['name'], va['language']))

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

    plt.savefig(config.get("MAL_GRAPH_FP"), bbox_inches='tight')
    plt.clf()

def score_graph(title, category, type="null"):

    res = api_request(title, category, type, stats=True)
    if not res:
        return None
    
    data = {"completed" : f"{res['completed']:,}", "on_hold" : f"{res['on_hold']:,}",
        "dropped" : f"{res['dropped']:,}", "total" : f"{res['total']:,}", "title" : res['title'], "url" : res['url']}
    
    if category == "manga":
        data["reading"] = f"{res['reading']:,}"
        data["plan_to_read"] = f"{res['plan_to_read']:,}"
    else:
        data["watching"] = f"{res['watching']:,}"
        data["plan_to_watch"] = f"{res['plan_to_watch']:,}"

    x = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    y = [score['votes'] for score in res['scores']]

    generate_graph(x, y, f"{res['title']} ({res['type']}) Vote distribution")
    return data