import discord
from discord.ext import commands
import configparser
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle


def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['kenma']

token = get_config()

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

guild_ids = [731539222141468673]



@client.event
async def on_ready():

    print("it started working")

@client.command()
async def cbutton(ctx):
    buttons = [
            manage_components.create_button(
                style=ButtonStyle.green,
                label="A Green Button", custom_id="hello"
            ),
          ]
    action_row = manage_components.create_actionrow(*buttons)
    await ctx.send("My Message", components=[action_row])

@slash.component_callback()
async def hello(ctx):
    await ctx.send(content="You pressed a button!")


client.run(token)