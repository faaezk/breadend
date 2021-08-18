import discord
from discord.ext import commands
import configparser
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import matchClass

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
async def lower(ctx, *, word):
    
    word = word.lower()
    await ctx.send(word)

@slash.slash(description="Information on last 5 games",
             guild_ids=guild_ids,
             options = [create_option(name="username", description="Enter Username (username#tag)", option_type=3, required=True),
             create_option(name="game", description="Select game to get info on", option_type=3, required=True, 
                choices=[create_choice(name="1",value="1"), create_choice(name="2",value="2"),
                         create_choice(name="3",value="3"),create_choice(name="4",value="4"), create_choice(name="5",value="5")]),

             create_option(name="type", description="Select type of information", option_type=3, required=True,
                choices=[create_choice(name="overview",value="overview"), create_choice(name="round-by-round",value="rounds")])])
async def games(ctx, username, game, type):

    if len(username.split('#')) != 2:
        await ctx.send("invalid player name")
    
    else:
        ign, tag = username.split('#')
        data = matchClass.get_data(ign.lower(), tag.lower(), game)

        if data == "invalid game index":
            await ctx.send("invalid game index")

        elif data == False:
            await ctx.send("Player not found")

        else:
            match = matchClass.Match(data['metadata']['map'], data['metadata']['mode'])

            match.addPlayers(data['players']['red'], 'red')
            match.addPlayers(data['players']['blue'], 'blue')

            for round in data['rounds']:
                tempRound = matchClass.Round(round['winning_team'], round['end_type'], 
                            round['bomb_planted'], round['bomb_defused'])

                tempRound.addEvents(round['player_stats'])
                match.addRound(tempRound)
            
            await ctx.send("please work")


client.run(token)