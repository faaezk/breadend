import discord
from discord.ext import commands
import weather
import configparser
import valorant_online
import graphs
import valorant

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['token']

token = get_config()

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print("it started working")

@client.command()
async def weatherz(ctx):
    john = weather.main()
    await ctx.send("Feels like " + str(john['main']['feels_like']) + " degrees today")

@client.command()
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

@client.command()
async def elolist(ctx, *, username):

    username = username.split('#')[0].lower()
    elolist = valorant.get_elolist(username)
    await ctx.send("```\n" + elolist + "\n```")

@client.command()
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

@client.command()
async def online(ctx):
    await ctx.send("```\nUnfortunately, the API is being weird so this command does not work at the moment.\n```")
    '''
    the_message = await ctx.send("please wait...")
    valorant_online.loadData()
    john = valorant_online.main()
    msg = ""

    for i in range(0, len(john)):

        if john[i][0] == "no parties" or john[i][0] == "Players Online:" or john[i][0] == "All players offline":
            msg += john[i][0] + '\n'

        elif john[i][0] == "Parties:":
            msg += '\n' + john[i][0] + '\n'
            
        else:  
            msg += john[i][0] + ": " + john[i][1] + '\n'

    await the_message.edit(content="```\n" + msg + "\n```")
    '''

@client.command()
async def add(ctx, *, username):

    username = username.lower()
    jg = valorant_online.addPlayer(username, False)

    if jg == False:
        await ctx.send("Player does not exist")
    elif jg == True:
        await ctx.send("Player has already been added")
    else:
        await ctx.send("Player added")

@client.command()
async def addonline(ctx, *, username):

    username = username.lower()
    jg = valorant_online.addPlayer(username, True)

    if jg == False:
        await ctx.send("Player does not exist")
    elif jg == True:
        await ctx.send("Player has already been added")
    else:
        await ctx.send("Player added")

@client.command()
async def remove(ctx, *, username):

    if ctx.author.id == 410771947522359296:
        username = username.lower()

        if valorant_online.removePlayer(username, False) == False:
            await ctx.send("Player not in list")

        else:
            await ctx.send("Player removed")
            
    else:
        await ctx.send("no.")

@client.command()
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
    msg = """Commands:
$leaderboard -> returns an elo leaderboard (up to 13 minutes old)
$leaderboard update -> returns the most recently updated elo leaderboard (slow)
$graph -> returns a graph of the player's elo over time
$elolist -> returns the elo values used in the graph
$online -> returns the player who are online from the list
$add -> adds the player to the database for leaderboard/graph/elolist
$addonline -> adds the player to the database for $online\n
Usage:
$graph username (not username#tag)
$elolist username (not username#tag)
$add username#tag name (name field is optional, if left blank, it'll use your username as the name)
$addonline username#tag name (name field optional)\n
Note: Being added to the online requires you to add valorant#API as a friend, after adding yourself
using $addonline, you will hopefully be send a friend request (don't send the friend request yourself)
for any further questions, ask faaez
oh and if the thingo unexpectedly starts sending you a friend request and you can't accept it, idk what's up with that"""

    await ctx.send("```\n" + msg + "\n```")

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