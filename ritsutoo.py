import discord
from discord.ext import commands
import configparser
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

client.run(token)