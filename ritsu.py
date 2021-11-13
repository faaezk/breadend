import discord
from discord.ext import commands
import configparser
import valorant
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

def get_config():
    c = configparser.ConfigParser()
    c.read('config.ini')

    return c['discord']['ritsu']

token = get_config()

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='!',help_command = help_command)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [731539222141468673]

@client.event
async def on_ready():
    print("it started working")

@client.command()
async def banner(ctx, *, username):
    username = username.split('#')

    if len(username) == 2:
        valorant.banner(username[0].lower(), username[1].lower())
        await ctx.send(file=discord.File('banner.png'))
    
    else:
        tag = valorant.get_tag(username[0].lower())
        
        if tag != "Player not found.":
            valorant.banner(username[0].lower(), tag)
            await ctx.send(file=discord.File('banner.png'))

        else:
            await ctx.send(content="```\n" + "Player not found, check syntax: (username#tag)" + "\n```")

@client.event
async def on_message(message):

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)

client.run(token)
