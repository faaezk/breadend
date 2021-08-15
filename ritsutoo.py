import discord
from discord.ext import commands
import configparser
import requests
import json

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['token']

token = get_config()

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print("it started working")

@client.command()
async def anime(ctx, *, title):

    await ctx.send("Getting info for " + title)

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


    embed = discord.Embed(title="{} ({})".format(anime['title_english'], anime['title_japanese']), url=anime['url'], 
                        description="Source: {}, Type: {}, Score: {}, Episodes: {}".format(anime['source'], anime['type'], anime['score'], ep_count))
    
    embed.set_image(url=anime['image_url'])
    embed.add_field(name="Airing Dates:", value=anime['aired']['string'])
    embed.add_field(name="Genres:", value=genres)
    embed.add_field(name="Sequel", value=sequel)
    embed.add_field(name="Opening Theme", value=opening_themes, inline=False)
    embed.add_field(name="Ending Theme", value=ending_themes, inline=False)
    embed.set_footer(text="Studios: {}, Licensors: {}".format(studios, licensors))
    await ctx.send(embed=embed)


client.run(token)