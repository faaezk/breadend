import matplotlib.pyplot as plt
import requests
import json

def animeSearch(title):

    try:
        response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1', timeout=5)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1', timeout=5)
        except:
            return False

    id = json.loads(response.text)
    if 'results' in id.keys():
        id = id['results'][0]['mal_id']
    else:
        return None
    
    try:
        response = requests.get(f'https://api.jikan.moe/v3/anime/{id}', timeout=5)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/anime/{id}', timeout=5)
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
        response = requests.get(f'https://api.jikan.moe/v3/search/character?q={name}&page=1', timeout=5)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/search/character?q={name}&page=1', timeout=5)
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


def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

def animeStats(title):
    
    try:
        response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1', timeout=5)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1', timeout=5)
        except:
            return False

    id = json.loads(response.text)

    name = id['results'][0]['title']
    url = id['results'][0]['url']

    if 'results' in id.keys():
        id = id['results'][0]['mal_id']
    else:
        return None


    try:
        response = requests.get(f'https://api.jikan.moe/v3/anime/{id}/stats', timeout=4)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/anime/{id}/stats', timeout=4)
        except:
            return False

    anime = json.loads(response.text)

    x = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    y = []
    y.append(anime['scores']['1']['votes'])
    y.append(anime['scores']['2']['votes'])
    y.append(anime['scores']['3']['votes'])
    y.append(anime['scores']['4']['votes'])
    y.append(anime['scores']['5']['votes'])
    y.append(anime['scores']['6']['votes'])
    y.append(anime['scores']['7']['votes'])
    y.append(anime['scores']['8']['votes'])
    y.append(anime['scores']['9']['votes'])
    y.append(anime['scores']['10']['votes'])

    plt.figure(figsize=(9, 6))
    plt.bar(x, y)
    
    plt.title(f'{name} Vote distribution')
    plt.xlabel('Scores')
    plt.ylabel('Votes')
    
    # Create names on the x axis
    plt.xticks(x)
    plt.yticks()
    addlabels(x, y)
    plt.savefig('/home/ubuntu/discord_bot/image.png', bbox_inches='tight')
    plt.clf()

    return {"watching":anime["watching"],"completed":anime["completed"],"on_hold":anime["on_hold"],
        "dropped":anime["dropped"],"plan_to_watch":anime["plan_to_watch"],"total":anime["total"],
        "title" : name, "url" : url}

def mangaSearch(title):

    try:
        response = requests.get(f'https://api.jikan.moe/v3/search/manga?q={title}&page=1', timeout=5)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/search/manga?q={title}&page=1', timeout=5)
        except:
            return False

    id = json.loads(response.text)
    if 'results' in id.keys():
        id = id['results'][0]['mal_id']
    else:
        return None
    
    try:
        response = requests.get(f'https://api.jikan.moe/v3/manga/{id}', timeout=5)
    except:
        try:
            response = requests.get(f'https://api.jikan.moe/v3/manga/{id}', timeout=5)
        except:
            return False

    manga = json.loads(response.text)

    if manga['volumes'] == None:
        vol_count = '?'
    else:
        vol_count = str(manga['volumes'])
    
    if manga['chapters'] == None:
        chap_count = '?'
    else:
        chap_count = str(manga['chapters'])


    genres = ""
    for genre in manga['genres']:
        genres += genre['name'] + ', '
    genres = genres[:-2]

    authors = ""
    for author in manga['authors']:
        authors += author['name'] + '\n'
    studios = authors[:-1]

    serializations = ""
    for serialization in manga['licensors']:
        serializations += serialization['name'] + ', '
    licensors = serializations[:-2]

    if genres == "":
        genres = "None"
    if studios == "":
        studios = "None"
    if licensors == "":
        licensors = "None"
    
    return {"vol_count" : vol_count, "chap_count" : chap_count, "genres" : genres, "publishing" : manga['published']['string'],
            "score" : manga['source'], "type" : manga['type'], "rank" : manga['rank'], "url" : manga['url'],
            "eng_title" : manga['title_english'], "jap_title" : manga['title_japanese'], "image_url" : manga['image_url'],
            "authors" : authors, "serialisations" : serializations}


if __name__ == '__main__':
    animeStats('bunny girl senpai')