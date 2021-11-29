import discord
from discord.ext import commands
import configparser
import valorant
import graphs
import playerclass
import elo_history_updater
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

@slash.slash(description="Lineup thing",
             guild_ids=guild_ids,
             options = [
             create_option(name="agent", description="Select agent to show lineup for", option_type=3, required=False, 
                        choices=[create_choice(name="Viper",value="viper")]),
             create_option(name="map", description="Select map to show lineup for", option_type=3, required=False, 
                        choices=[create_choice(name="Ascent",value="ascent")])])
async def lineup(ctx, agent="", map=""):

    if agent != "" and map != "":
        await ctx.send(f'https://atomic-potatos.github.io/Valorant-Lineups/agents/{agent}/{map}.html')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))

    await client.process_commands(message)


client.run(token)