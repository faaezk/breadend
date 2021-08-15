import discord
from discord.ext import commands
import configparser
import valorant_online
import graphs
import valorant
import requests
import json

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['token'], c['cat']['api'], c['NASA']['api']

token = get_config()[0]

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='$',help_command = help_command)

@client.event
async def on_ready():
    print("it started working")

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

@client.command()
async def nasa(ctx):
    url = "https://api.nasa.gov/planetary/apod"

    payload={}
    files={}
    headers = {
    'Content-Type': 'application/json',
    'x-api-key': get_config()[2]
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    loaded = json.loads(response.text)
    embed = discord.Embed(title="Astronomy Photo of The Day", description=loaded['title'])
    embed.set_image(url=loaded['url'])
    embed.set_footer(text = "Copyright: {}, {}".format(loaded['copyright'], loaded['date']))

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

    flag = graphs.double_graph(players)
    
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
    await ctx.send("```\n" + elolist + "\n```")

@client.command(
    help="Syntax: $stats username#tag", 
    brief="Returns some comp statistics from each Act")
async def stats(ctx, *, username):

    username = username.split('#')
    if len(username) == 2:
        fields = valorant.stats(username[0].lower(), username[1].lower())
        embed=discord.Embed(title = f'{username[0]}\'s Competitive Statistics', url = "https://youtu.be/MtN1YnoL46Q", description="", color=0x00f900)
        for field in fields:
            embed.add_field(name = field[0], value = field[1], inline = True)

        embed.set_footer(text = "unlucky")
        await ctx.send(embed = embed)

    else:
        await ctx.send("```\n" + "Player not found, check syntax: (username#tag)" + "\n```")

@client.command(
    help="Optional argument to update leaderboard with newest data: 'update'\nSyntax: $leaderboard or $leaderboard update", 
    brief="Returns a MMR leaderboard (updates every 13 minutes)")
async def leaderboard(ctx, *, command="john"):

    if command.lower() == 'update':
        the_message = await ctx.send("this is gonna take a while...")
        john = valorant.elo_leaderboard()
        await the_message.edit(content="```\n" + john + "\n```")
         
    else:
        john = "this is like, potentially up to 13 minutes old\n"
        f = open("leaderboard.txt", "r")
        for x in f:
            john += x
        f.close()

        await ctx.send("```\n" + john + "\n```")

@client.command(
    help="See $addonline to be added to the list", 
    brief="Returns the player who are online from the list")
async def online(ctx):
    await ctx.send("```\nUnfortunately, the API is being weird so this command does not work at the moment.\n```")

    # the_message = await ctx.send("please wait...")
    # valorant_online.loadData()
    # john = valorant_online.main()
    # msg = ""

    # for i in range(0, len(john)):

    #     if john[i][0] == "no parties" or john[i][0] == "Players Online:" or john[i][0] == "All players offline":
    #         msg += john[i][0] + '\n'

    #     elif john[i][0] == "Parties:":
    #         msg += '\n' + john[i][0] + '\n'
            
    #     else:  
    #         msg += john[i][0] + ": " + john[i][1] + '\n'

    # await the_message.edit(content="```\n" + msg + "\n```")

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
    help="""Syntax: $addonline username#tag name (name field optional)
Note: Being added to the online requires you to add valorant#API as a friend, after adding yourself,
you will hopefully be send a friend request. (don't send the friend request yourself)""", 
    brief="Adds the player to the list for $online")
async def addonline(ctx, *, username):

    username = username.lower()
    jg = valorant_online.addPlayer(username, True)

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
    embed.add_field(name = "leaderboard", value = "Returns a MMR leaderboard (updates every 13 minutes)\nOptional argument: update", inline = False)
    embed.add_field(name = "multigraph", value = "Returns a graph with multiple player's elo over time\nSyntax: $multigraph username1, username2, username3\n (not username#tag)", inline = False)
    embed.add_field(name = "stats", value = "Returns some comp statistics from each Act\nSyntax: $stats username#tag", inline = False)

    embed.set_footer(text = "unlucky")
    await ctx.send(embed = embed)


@client.command()
async def gettag(ctx, *, user):
    user = user.lower()
    await ctx.send(f'{user}#{valorant.get_tag(user)}')

@client.command()
async def anime(ctx, *, title):
    await ctx.send("Getting info for " + title)
    
    response = requests.get(f'https://api.jikan.moe/v3/search/anime?q={title}&page=1', timeout=5)
    id = json.loads(response.text)['results'][0]['mal_id']

    response = requests.get(f'https://api.jikan.moe/v3/anime/{id}', timeout=5)
    anime = json.loads(response.text)

    if anime['episodes'] == None:
        ep_count = '?'
    else:
        ep_count = str(anime['episodes'])

    opening_themes = ""
    ending_themes = ""

    for theme in anime['opening_themes']:
        if len(opening_themes) > 989:
            opening_themes = opening_themes[:-(len(last) + 1)]
            opening_themes += "more at MyAnimeList (link in title)"
            break
        opening_themes += theme + '\n'
        last = theme
    
    for theme in anime['ending_themes']:
        if len(ending_themes) > 989:
            ending_themes = ending_themes[:-(len(last) + 1)]
            ending_themes += "more at MyAnimeList (link in title)"
            break
        ending_themes += theme + '\n'
        last = theme

    sequel = ""
    if 'Sequel' in anime['related'].keys():
        for i in range(0, len(anime['related']['Sequel'])):
            if len(anime['related']['Sequel']) == 1:
                sequel = anime['related']['Sequel'][i]['name'] + '\n'
            else:
                sequel += str(i + 1) + '. ' + anime['related']['Sequel'][i]['name'] + '\n'

        sequel = sequel[:-1]

    genres = ""
    for genre in anime['genres']:
        genres += genre['name'] + ', '
    genres = genres[:-2]

    studios = ""
    for studio in anime['studios']:
        studios += studio['name'] + ', '
    studios = studios[:-2]

    licensors = ""
    for licensor in anime['licensors']:
        licensors += licensor['name'] + ', '
    licensors = licensors[:-2]

    if opening_themes == "":
        opening_themes = "None"
    if ending_themes == "":
        ending_themes = "None"
    if sequel == "":
        sequel = "None"
    if genres == "":
        genres = "None"
    if studios == "":
        studios = "None"
    if licensors == "":
        licensors = "None"


    embed = discord.Embed(title="{} ({})".format(anime['title_english'], anime['title_japanese']), url=anime['url'], 
                        description="Source: {}, Type: {}, Score: {}, Episodes: {}".format(anime['source'], anime['type'], anime['score'], ep_count))
    
    embed.set_image(url=anime['image_url'])
    embed.add_field(name="Airing Dates:", value=anime['aired']['string'])
    embed.add_field(name="Genres:", value=genres)
    embed.add_field(name="Sequel", value=sequel)
    embed.add_field(name="Opening Theme", value=opening_themes, inline=False)
    embed.add_field(name="Ending Theme", value=ending_themes, inline=False)
    embed.set_footer(text="Studios: {}, Licensors: {}".format(studios, licensors))
    await ctx.send(embed=embed)

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