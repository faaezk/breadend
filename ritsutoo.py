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

    url2 = anime['url']
    image = anime['image_url']
    OP = anime['opening_themes']

    embed = discord.Embed(title=anime['title'], url=url2)
    embed.add_field(name="Opening Theme", value=OP)
    embed.set_image(url=image)

    await ctx.send(embed=embed)


client.run(token)