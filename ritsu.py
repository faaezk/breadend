import discord
from discord.ext import commands
import configparser
import valorant
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

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

@slash.slash(description="MMR history list",
             guild_ids=guild_ids,
             options = [
             create_option(name="username", description="enter username", option_type=3, required=True)])
async def tester(ctx, username=""):
    
    username = username.split('#')[0].lower()
    elolist = valorant.get_elolist(username)
    if elolist == None:
        await ctx.send("No comp games recorded")
    
    elif elolist == False:
        await ctx.send("Player not found")
    
    else:
        await ctx.send("```\n" + elolist + "\n```")

@client.event
async def on_message(message):

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)

client.run(token)
