import discord
from discord.ext import commands
import configparser
import random

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['token2']

token = get_config()

client = commands.Bot(command_prefix=';')

@client.event
async def on_ready():
    print("it started working")

@client.command()
async def ping(ctx):
    await ctx.send(f'bong {round(client.latency * 1000)} ms')

@client.command(aliases = ['8ball', 'balls'])
async def _8ball(ctx, *, question):
    responses = ['no', 'your mother', 'no', 'balls']
    await ctx.send(f'question: {question}\nAns: {random.choice(responses)}')

client.run(token)