import discord
from discord.ext import commands
import configparser
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
import Match

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

@slash.slash(description="Information on last 5 games",
             guild_ids=guild_ids,
             options = [create_option(name="username", description="Enter Username (username#tag)", option_type=3, required=True),
             create_option(name="Game", description="Select game to get info on", option_type=3, required=True),
             create_option(name="Type", description="Select type of information", option_type=3, required=True,
              choices=[
                  create_choice(name="Overview",value="Overview"),
                  create_choice(name="Round-by-round",value="rounds")])])
async def games(ctx, *, game = "", Type = ""):
    

    if game == "":

        data = Match.get_data('fakinator', '4269')
        game = Game(data['metadata']['map'], data['metadata']['mode'])

        game.addPlayers(data['players']['red'], 'red')
        game.addPlayers(data['players']['blue'], 'blue')

        for round in data['rounds']:
            tempRound = Round(round['winning_team'], round['end_type'], 
                        round['bomb_planted'], round['bomb_defused'])

            tempRound.addEvents(round['player_stats'])
            game.addRound(tempRound)


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