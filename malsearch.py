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
    
    return {"episode count" : ep_count, "sequel" : sequel, "genres" : genres, "Airing Dates" : anime['aired']['string'],
            "source" : anime['source'], "type" : anime['type'], "score" : anime['score'], "url" : anime['url'],
            "eng_title" : anime['title_english'], "jap_title" : anime['title_japanese'], "image url" : anime['image_url'],
            "studios" : studios, "licensors" : licensors,"opening themes": opening_themes, "ending themes" : ending_themes}