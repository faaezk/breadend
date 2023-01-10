import discord
from discord.ext import commands
import configparser
import graphs
import valorant
import mmr_history_updater
import requests
import json
import malsearch
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import random
import playerclass
from discord import app_commands

def get_config():
    c = configparser.ConfigParser()
    c.read('config.ini')
    return c['discord']['token'], c['cat']['api']

token = get_config()[0]
intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='$',help_command = help_command, intents=intents)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [509314650265878530, 731539222141468673]

@client.event
async def on_ready():
    print("it started working")
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"yo {interaction.user.mention}", ephemeral=True)


@client.tree.command(name="rps")
@app_commands.choices(choices=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
    ])
async def rps(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    if (choices.value == 'rock'):
        counter = 'paper'
    elif (choices.value == 'paper'):
        counter = 'scissors'
    else:
        counter = 'rock'

    await interaction.response.send_message(f"yo {counter}")
    
@client.event
async def on_message(message):
    await client.process_commands(message)

client.run(token)