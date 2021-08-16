import requests
import json

def animeSearch(title):
    response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1', timeout=5)
    id = json.loads(response.text)['results'][0]['mal_id']

    response = requests.get(f'https://api.jikan.moe/v3/anime/{id}', timeout=5)
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
    
    response = requests.get(f'https://api.jikan.moe/v3/search/character?q={name}&page=1', timeout=5)
    id = json.loads(response.text)['results'][0]['mal_id']

    response = requests.get(f'https://api.jikan.moe/v3/character/{id}', timeout=5)
    character = json.loads(response.text)

    info = character['about']

    anime = ""
    for show in character['animeography']:
        anime += show['name'] + '\n'

    manga = ""
    for book in character['mangaography']:
        manga += book['name'] + '\n'

    voice_actors = ""
    for va in character['voice_actors']:
        voice_actors += va['language'] + ': ' + va['name'] + '\n'

    if len(info) > 970:
        info = info[0:970]
        info += "...\n\nMore at MyAnimeList (link in title)"

    if len(anime) > 970:
        anime = anime[0:970]
        anime += "...\n\nMore at MyAnimeList (link in title)"

    if len(manga) > 970:
        manga = manga[0:970]
        manga += "...\n\nMore at MyAnimeList (link in title)"

    if len(voice_actors) > 970:
        voice_actors = voice_actors[0:970]
        voice_actors += "...\n\nMore at MyAnimeList (link in title)"

    return {"url" : character['url'], "image_url" : character['image_url'], "name" : character['name'],
            "voice_actors" : voice_actors, "anime" : anime, "manga" : manga, "description" : info,
            "member_favourites" : character["member_favorites"]}