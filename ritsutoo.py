import discord
from discord.ext import commands
import weather
import configparser
import valorant_online
import graphs
import valorant

def get_config():
    c = configparser.ConfigParser()
    c.read('config.ini')

    return c['discord']['token2']

token = get_config()

client = commands.Bot(command_prefix=';')

@client.event
async def on_ready():
    print("it started working")

@client.command()
async def ping(ctx):
    await ctx.send(f'bong {round(client.latency * 1000)} ms')

@client.command()
async def elolist(ctx, *, username):

    username = username.lower()
    elolist = valorant.get_elolist(username)
    await ctx.send("```\n" + elolist + "\n```")

@client.command()
async def weather(ctx):
    john = weather.main()
    await ctx.send("Feels like " + str(john['main']['feels_like']) + " degrees today")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)


client.run(token)