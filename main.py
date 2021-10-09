import discord
from discord.ext import commands
import configparser
import valorant_online
import graphs
import valorant
import requests
import json
import malsearch
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import random

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['token'], c['cat']['api']

token = get_config()[0]

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='$',help_command = help_command)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [509314650265878530]

@client.event
async def on_ready():
    print("it started working")

@slash.slash(description="Choices for Valorant",
             guild_ids=guild_ids,
             options = [
             create_option(name="randomise", description="returns random thing", option_type=3, required=False, 
                        choices=[create_choice(name="account",value="account"), create_choice(name="gamemode",value="gamemode"),
                        create_choice(name="weapon",value="weapon"), create_choice(name="agent",value="agent"),
                        create_choice(name="map",value="map")]),
             create_option(name="tactic", description="returns the plays for this round", option_type=3, required=False, 
                        choices=[create_choice(name="attacking",value="attacking"), create_choice(name="defending",value="defending")])])

async def choice(ctx, randomise="", tactic=""):
    
    if randomise == "account":
        await ctx.send(random.choice(['Smurfs', 'Smurfs', 'Smurfs', 'Smurfs', 'Mains', 'Mains', 'Mains', 'Mains', 'Mains', 'Mains']))
    
    if randomise == "gamemode":
        await ctx.send(random.choice(['Unrated', 'Competitive']))

    if randomise == "weapon":
        sidearm = ["Classic", "Shorty", "Frenzy", "Ghost", "Sheriff"]
        SMG = ["Stinger", "Spectre"]
        Shotgun = ["Bucky"]
        Rifle = ["Bulldog", "Guardian", "Phantom", "Vandal"]
        Sniper = ["Marshal", "Operator"]
        MG = ["Ares", "Odin"]
        selected = random.choice([sidearm, SMG, Shotgun, Rifle, Sniper, MG])
        await ctx.send(random.choice(selected))
    
    if randomise == "agent":
        await ctx.send(random.choice(["Astra", "Breach", "Brimstone", "Cypher", "Jett", "Killjoy", "Kay/O"
                                     "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", "Viper", "Yoru"]))

    if randomise == "map":
        await ctx.send(random.choice(["Bind", "Haven", "Split", "Ascent", "Icebox", "Breeze"]))

    if tactic == "attacking":
        await ctx.send(random.choice(["Rush A", "Rush B", "Rush C", "Cowboy Time", "Hide in spawn", "Split push",
                                        "Odin go brrr", "just ff", "Camp in corners", "Snipers only", "Pistol Prodigy"]))
    if tactic == "defending":
        await ctx.send(random.choice(["Everyone on A", "Everyone on B", "Everyone on C", "Cowboy Time", "Hide in spawn till plant",
                                        "Odin go brrr", "just ff", "Camp in corners", "Snipers only", "Pistol Prodigy"]))

@client.command()
async def cat(ctx):
    url = "https://api.thecatapi.com/v1/images/search?format=json"

    payload={}
    files={}
    headers = {
    'Content-Type': 'application/json',
    'x-api-key': get_config()[1]
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    embed = discord.Embed(title="cat")
    embed.set_image(url=json.loads(response.text)[0]['url'])

    await ctx.send(embed=embed)

@client.command(
    help="Syntax: $graph username or $graph username#tag", 
    brief="Returns a graph of the player's elo over time")
async def graph(ctx, *, username):

    username = username.split('#')[0].lower()
    flag = graphs.make_graph(username)
    
    if flag == False:
        await ctx.send("Player not found")

    elif flag == None:
        await ctx.send("Not enough data to plot graph")

    else:
        with open("/home/ubuntu/discord_bot/elo_graphs/{}.png".format(username), 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

@client.command(
    help="Where players is a list of username's (not username#tag) seperated by commas.\nSyntax: $multigraph username1, username2, username3", 
    brief="Returns a graph with multiple player's elo over time")
async def multigraph(ctx, *, players):

    players = players.replace(" ", "").split(',')

    for i in range(0, len(players)):
        players[i] = players[i].lower()

    flag = graphs.multigraph(players)
    
    if flag == False:
        await ctx.send("Player not found")

    elif flag == None:
        await ctx.send("Not enough data to plot graph")

    else:
        with open("/home/ubuntu/discord_bot/elo_graphs/multigraph.png", 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

@client.command(
    help="Syntax: $elolist username or $elolist username#tag", 
    brief="Returns the elo values used in the graph")
async def elolist(ctx, *, username):

    username = username.split('#')[0].lower()
    elolist = valorant.get_elolist(username)
    if elolist == None:
        await ctx.send("No comp games recorded")
    else:
        await ctx.send("```\n" + elolist + "\n```")


@slash.slash(description="Ranked statistics for all acts",
             guild_ids=guild_ids,
             options = [
             create_option(name="username", description="enter username (user#tag)", option_type=3, required=True)])
async def stats(ctx, username=""):

    the_message = await ctx.send("fetching stats...")
    username = username.split('#')

    if len(username) == 2:

        fields = valorant.stats(username[0].lower(), username[1].lower())
        embed=discord.Embed(title = f'{username[0]}\'s Competitive Statistics', url = "https://youtu.be/MtN1YnoL46Q", description="", color=0x00f900)

        for field in fields:
            embed.add_field(name = field[0], value = field[1], inline = True)

        embed.set_footer(text = "unlucky")
        await the_message.edit(embed = embed)
    
    else:
        tag = valorant.get_tag(username[0].lower())
        
        if tag != "Player not found.":
            fields = valorant.stats(username[0].lower(), tag)
            embed=discord.Embed(title = f'{username[0]}\'s Competitive Statistics', url = "https://youtu.be/MtN1YnoL46Q", description="", color=0x00f900)

            for field in fields:
                embed.add_field(name = field[0], value = field[1], inline = True)

            await the_message.edit(embed = embed)

        else:
            await the_message.edit(content="```\n" + "Player not found, check syntax: (username#tag)" + "\n```")


@slash.slash(description="Valorant Leaderboards",
             guild_ids=guild_ids,
             options = [
             create_option(name="options", description="Region/options for leaderboard (leave blank for local)", option_type=3, required=False, 
                        choices=[create_choice(name="Update local leaderboard",value="update"), create_choice(name="Asia Pacific",value="ap"),
                        create_choice(name="Europe",value="eu"), create_choice(name="Korea",value="kr"),
                        create_choice(name="North America",value="na")])])
async def leaderboard(ctx, options=""):
    
    if options == "":
        john = "this is like, potentially up to 13 minutes old\n"
        f = open("leaderboard.txt", "r")
        for x in f:
            john += x
        f.close()

        await ctx.send("```\n" + john + "\n```")
    
    if options == "update":
        the_message = await ctx.send("this is gonna take a while...")
        john = valorant.elo_leaderboard()
        await the_message.edit(content="```\n" + john + "\n```")

    if options == "ap" or options == "eu" or options == "kr" or options == "na":

        regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}
        
        the_message = await ctx.send("fetching leaderboard...")
        rleaderboard = valorant.region_leaderboard(options)

        if rleaderboard:
            contents = f'{regions[options]} Ranked Leaderboard\n'
            contents += rleaderboard
            await the_message.edit(content="```\n" + contents + "\n```")

@client.command(
    help="No longer works", 
    brief="Returns the player who are online from the list")
async def online(ctx):
    await ctx.send("Unfortunately, the API deprecated this endpoint so the command no longer works.")


@client.command(
    help="Syntax: $add username#tag name (name field is optional)", 
    brief="Adds the player to the database for leaderboard/graph/elolist")
async def add(ctx, *, username):

    username = username.lower()
    jg = valorant_online.addPlayer(username, False)

    if jg == False:
        await ctx.send("Player does not exist")
    elif jg == True:
        await ctx.send("Player has already been added")
    else:
        await ctx.send("Player added")

@client.command(
    help="ask Faaez (Fakinator) if you wanna be removed", 
    brief="Removes the player from the database")
async def remove(ctx, *, username):

    if ctx.author.id == 410771947522359296:
        username = username.lower()

        if valorant_online.removePlayer(username, False) == False:
            await ctx.send("Player not in list")

        else:
            await ctx.send("Player removed")
            
    else:
        await ctx.send("no.")

@client.command(
    help="ask Faaez (Fakinator) if you wanna be removed", 
    brief="Removes the player from the online list")
async def removeonline(ctx, *, username):

    if ctx.author.id == 410771947522359296:
        username = username.lower()

        if valorant_online.removePlayer(username, True) == False:
            await ctx.send("Player not in list")

        else:
            await ctx.send("Player removed")
            
    else:
        await ctx.send("no.")
    
@client.command()
async def valhelp(ctx):
    embed=discord.Embed(title = "List of Commands", url = "https://youtu.be/MtN1YnoL46Q", description="", color=0x00f900)
    
    embed.add_field(name = "add", value = "Adds the player to the database for leaderboard/graph/elolist\nSyntax: $add username#tag name (name field is optional)", inline = False)
    embed.add_field(name = "elolist", value = "Returns the elo values used in the graph\nSyntax: $elolist username or $elolist username#tag", inline = False)
    embed.add_field(name = "graph", value = "Returns a graph of the player's elo over time\nSyntax: $graph username or $graph username#tag", inline = False)
    embed.add_field(name = "multigraph", value = "Returns a graph with multiple player's elo over time\nSyntax: $multigraph username1, username2, username3\n (not username#tag)", inline = False)
    embed.add_field(name = "stats", value = "Returns some comp statistics from each Act\nSyntax: $stats username#tag", inline = False)

    embed.set_footer(text = "unlucky")
    await ctx.send(embed = embed)


@client.command()
async def gettag(ctx, *, user):
    user = user.lower()
    if valorant.get_tag(user) == "Player not found.":
        await ctx.send("Player not in database. add using $add")
    else:
        await ctx.send(f'{user}#{valorant.get_tag(user)}')

@slash.slash(description="search MAL database",
             guild_ids=guild_ids,
             options = [create_option(name="anime_title", description="Enter an anime to search for", option_type=3, required=False),
             create_option(name="manga_title", description="Enter an manga to search for", option_type=3, required=False),
             create_option(name="character", description="Enter a character to search for", option_type=3, required=False),
             create_option(name="anime_stats", description="Enter an anime to get stats for", option_type=3, required=False),
             create_option(name="manga_stats", description="Enter an manga to get stats for", option_type=3, required=False)])
async def search(ctx, *, anime_title = "", manga_title = "", character = "", anime_stats = "", manga_stats = ""):
    
    if anime_title != "":
        msg = await ctx.send("Getting info for " + anime_title)
        anime = malsearch.animeSearch(anime_title)

        if anime == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif anime == None:
            await ctx.send("Anime not found.")

        else:
            embed = discord.Embed(title="{} ({})".format(anime['eng_title'], anime['jap_title']), url=anime['url'], 
            description="Source: {}, Type: {}, Score: {}, Episodes: {}".format(anime['source'], anime['type'], anime['score'], anime["ep_count"]))

            embed.set_image(url=anime['image_url'])
            embed.add_field(name="Airing Dates:", value=anime["Airing_Dates"])
            embed.add_field(name="Genres:", value=anime["genres"])
            embed.add_field(name="Sequel", value=anime["sequel"])
            embed.add_field(name="Synopsis:", value=anime["synopsis"])
            embed.add_field(name="Opening Theme", value=anime["opening_themes"], inline=False)
            embed.add_field(name="Ending Theme", value=anime["ending_themes"], inline=False)
            embed.set_footer(text="Studios: {}, Licensors: {}".format(anime["studios"], anime["licensors"]))
            await msg.edit(content="", embed=embed)

    if manga_title != "":
        msg = await ctx.send("Getting info for " + manga_title)
        manga = malsearch.mangaSearch(manga_title)

        if manga == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif manga == None:
            await ctx.send("Manga not found.")

        else:
            embed = discord.Embed(title="{} ({})".format(manga['eng_title'], manga['jap_title']), url=manga['url'], 
            description="Type: {}, Score: {}, Volumes: {}, Chapters: {}".format(manga['type'], manga['score'], manga["vol_count"], manga["chap_count"]))

            embed.set_image(url=manga['image_url'])
            embed.add_field(name="Publishing Dates:", value=manga["publishing"])
            embed.add_field(name="Genres:", value=manga["genres"])
            embed.add_field(name="Authors:", value=manga["authors"])
            embed.add_field(name="Synopsis:", value=manga["synopsis"])
            embed.set_footer(text="Serialisations: {}".format(manga["serialisations"]))
            await msg.edit(content="", embed=embed)

    if character != "":
        msg = await ctx.send("Getting info for " + character)
        character = malsearch.characterSearch(character)

        if character == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif character == None:
            await ctx.send("Character not found.")

        else:
            embed = discord.Embed(title=character['name'], url=character['url'],
                                    description="Member favourites: " + str(character['member_favourites']))

            embed.set_image(url=character['image_url'])
            embed.add_field(name="Description", value=character["description"], inline=False)
            embed.add_field(name="Anime:", value=character["anime"], inline=False)
            embed.add_field(name="Manga:", value=character["manga"], inline=False)
            embed.add_field(name="Voice Actors:", value=character["voice_actors"], inline=False)
            
            await msg.edit(content="", embed=embed)

    if anime_stats != "":
        msg = await ctx.send("Getting stats for " + anime_stats)
        anime = malsearch.animeStats(anime_stats)

        if anime == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif anime == None:
            await ctx.send("Character not found.")

        else:
            file=discord.File(fp="/home/ubuntu/discord_bot/image.png", filename='image.png')
            embed = discord.Embed(title=anime['title'], url=anime['url'])

            embed.set_image(url="attachment://image.png")

            embed.add_field(name="Other stats:", 
            value="Completed: {}\nWatching: {}\nPlan to watch: {}\nDropped: {}\nOn Hold: {}\nTotal: {}".format(
                anime["completed"], anime["watching"], anime["plan_to_watch"], anime["dropped"],
                anime["on_hold"], anime["total"]),
            inline=False)
            
            await msg.edit(content="", file=file, embed=embed)

    if manga_stats != "":
        msg = await ctx.send("Getting stats for " + manga_stats)
        manga = malsearch.mangaStats(manga_stats)

        if manga == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif manga == None:
            await ctx.send("Character not found.")

        else:
            file=discord.File(fp="/home/ubuntu/discord_bot/image.png", filename='image.png')
            embed = discord.Embed(title=manga['title'], url=manga['url'])

            embed.set_image(url="attachment://image.png")

            embed.add_field(name="Other stats:", 
            value="Completed: {}\nReading: {}\nPlan to read: {}\nDropped: {}\nOn Hold: {}\nTotal: {}".format(
                manga["completed"], manga["reading"], manga["plan_to_read"], manga["dropped"],
                manga["on_hold"], manga["total"]),
            inline=False)
            
            await msg.edit(content="", file=file, embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    if "wow" in message.content.lower() and message.author.id == 203311457666990082:
        await message.add_reaction("<:stevens:785800069957943306>")
    
    await client.process_commands(message)


client.run(token)