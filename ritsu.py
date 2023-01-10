from discord.ext import commands
import configparser
import discord
from discord import app_commands

def get_config():
    c = configparser.ConfigParser()
    c.read('config.ini')
    return c['discord']['ritsu']

token = get_config()
intents = discord.Intents.default() 
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild_id = 731539222141468673

# sync the slash command to your server
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    # print "ready" in the console when the bot is ready to work
    print("ready")

# make the slash command
@tree.command(name="name", description="description", guild=discord.Object(id=guild_id))
async def slashing_commanding(int: discord.Interaction, input: str):    
    await int.response.send_message("command" + input)

# run the bot
client.run(token)