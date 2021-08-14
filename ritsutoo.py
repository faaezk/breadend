import discord
from discord.ext import commands
import configparser
from jikanpy import jikan

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
    search_result = jikan.search('anime', title)
    id = search_result['results'][0]['mal_id']

    anime = jikan.anime(id)

    score = anime['score']
    ep_count = anime['episodes']
    dates = anime['aired']['string']

    opening_themes = anime['opening_themes']
    ending_themes = anime['ending_themes']

    sequel = ""
    if 'Sequel' in anime['related'].keys():
        for x in anime['related']['Sequel']:
            sequel += x['name'] 
    if sequel == "":
        sequel = "None"

    genres = ""
    for genre in anime['genres']:
        genres += genre['name']

    embed = discord.Embed(title=anime['title'], url=anime['url'], description="Score: {}, Episodes: {}".format(score, ep_count))
    embed.add_field(name="Opening Theme", value=opening_themes)
    embed.add_field(name="Ending Theme", value=ending_themes)
    embed.add_field(name="Airing Dates:", value=dates)
    embed.add_field(name="Sequel", value=sequel)
    embed.add_field(name="Genres:", value=genres)

    embed.set_image(url=anime['image_url'])
    embed.set_footer(text="Source: Myanimelist")

    await ctx.send(embed=embed)


client.run(token)