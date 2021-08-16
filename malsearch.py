from discord.channel import VocalGuildChannel
import requests
import json

def animeSearch(title):

    try:
        response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1&limit=1', timeout=3)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1&limit=1', timeout=3)
        except:
            return False

    id = json.loads(response.text)
    if 'results' in id.keys():
        id = id['results'][0]['mal_id']
    else:
        return None
    
    try:
        response = requests.get(f'https://api.jikan.moe/v3/anime/{id}', timeout=4)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/anime/{id}', timeout=4)
        except:
            return False

    anime = json.loads(response.text)

    if anime['episodes'] == None:
        ep_count = '?'
    else:
        ep_count = str(anime['episodes'])

    opening_themes = ""
    ending_themes = ""

    for theme in anime['opening_themes']:
        if len(opening_themes) > 989:
            opening_themes = opening_themes[:-(len(last) + 1)]
            opening_themes += "more at MyAnimeList (link in title)"
            break
        opening_themes += theme + '\n'
        last = theme
    
    for theme in anime['ending_themes']:
        if len(ending_themes) > 989:
            ending_themes = ending_themes[:-(len(last) + 1)]
            ending_themes += "more at MyAnimeList (link in title)"
            break
        ending_themes += theme + '\n'
        last = theme

    sequel = ""
    if 'Sequel' in anime['related'].keys():
        for i in range(0, len(anime['related']['Sequel'])):
            if len(anime['related']['Sequel']) == 1:
                sequel = anime['related']['Sequel'][i]['name'] + '\n'
            else:
                sequel += str(i + 1) + '. ' + anime['related']['Sequel'][i]['name'] + '\n'

        sequel = sequel[:-1]

    genres = ""
    for genre in anime['genres']:
        genres += genre['name'] + ', '
    genres = genres[:-2]

    studios = ""
    for studio in anime['studios']:
        studios += studio['name'] + ', '
    studios = studios[:-2]

    licensors = ""
    for licensor in anime['licensors']:
        licensors += licensor['name'] + ', '
    licensors = licensors[:-2]

    if opening_themes == "":
        opening_themes = "None"
    if ending_themes == "":
        ending_themes = "None"
    if sequel == "":
        sequel = "None"
    if genres == "":
        genres = "None"
    if studios == "":
        studios = "None"
    if licensors == "":
        licensors = "None"
    
    return {"ep_count" : ep_count, "sequel" : sequel, "genres" : genres, "Airing_Dates" : anime['aired']['string'],
            "source" : anime['source'], "type" : anime['type'], "score" : anime['score'], "url" : anime['url'],
            "eng_title" : anime['title_english'], "jap_title" : anime['title_japanese'], "image_url" : anime['image_url'],
            "studios" : studios, "licensors" : licensors,"opening_themes": opening_themes, "ending_themes" : ending_themes}



def characterSearch(name):
    
    try:
        response = requests.get(f'https://api.jikan.moe/v3/search/character?q={name}&page=1&limit=1', timeout=3)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/search/character?q={name}&page=1&limit=1', timeout=3)
        except:
            return False
    
    id = json.loads(response.text)
    if 'results' in id.keys():
        id = id['results'][0]['mal_id']
    else:
        return None

    try:
        response = requests.get(f'https://api.jikan.moe/v3/character/{id}', timeout=4)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/character/{id}', timeout=4)
        except:
            return False

    character = json.loads(response.text)

    info = character['about']

    anime = ""
    for show in character['animeography']:

        if len(anime) > 989:
            anime = anime[:-(len(last))]
            anime += "more at MyAnimeList (link in title)"
            break
        anime += show['name'] + '\n'
        last = show['name'] + '\n'

    manga = ""
    for book in character['mangaography']:

        if len(manga) > 989:
            manga = manga[:-(len(last))]
            manga += "more at MyAnimeList (link in title)"
            break

        manga += book['name'] + '\n'
        last = book['name'] + '\n'


    voice_actors = ""
    for va in character['voice_actors']:

        if len(voice_actors) > 989:
            voice_actors = voice_actors[:-(len(last))]
            voice_actors += "More at MyAnimeList (link in title)"
            break

        voice_actors += va['language'] + ': ' + va['name'] + '\n'
        last = va['language'] + ': ' + va['name'] + '\n'

    if len(info) > 980:
        info = info[0:980]
        info += "...\nMore at MyAnimeList (link in title)"

    if anime == '':
        anime = "None"
    if voice_actors == '':
        voice_actors = "None"
    if manga == '':
        manga = "None"
    if info == '':
        info = "None"

    return {"url" : character['url'], "image_url" : character['image_url'], "name" : character['name'],
            "voice_actors" : voice_actors, "anime" : anime, "manga" : manga, "description" : info,
            "member_favourites" : character["member_favorites"]}

