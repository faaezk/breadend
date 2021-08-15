import discord
from discord.ext import commands
import configparser
import requests
import json
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['ritsu']

token = get_config()

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print("it started working")

@slash.slash(description="pong ping.")
async def pong(ctx):
    await ctx.send("ping")

@slash.slash(name="no",
             description="This is just a test command, nothing more.",
             options=[
               create_option(
                 name="BOHN",
                 description="This is the first option we have.",
                 option_type=3,
                 required=False,
                 choices=[
                  create_choice(
                    name="ChoiceOne",
                    value="DOGE!"
                  ),
                  create_choice(
                    name="ChoiceTwo",
                    value="NO DOGE"
                  )
                ]
               )
             ])
async def goula(ctx, optone: str):
  await ctx.send(content=f"Wow, you actually chose {optone}? :(")


client.run(token)