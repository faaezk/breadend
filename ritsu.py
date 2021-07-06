import discord
from discord.ext import commands
import valorant
import configparser
import graphs
import valorant_online
import schedule

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['token2']

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('=hello'):
        await message.channel.send('Hello!')

    if message.content.lower().startswith('=leaderboard'):
        john = valorant.elo_leaderboard()
        await message.channel.send("```\n" + john + "\n```")

    if message.content.lower().startswith('=graph'):

        themessage = message.content.lower()
        username = themessage[6:].strip()
        flag = graphs.make_graph(username)
        
        if flag == False:
            await message.channel.send("Player not found")

        elif flag == None:
            await message.channel.send("Not enough data to plot graph")

        else:
            with open("/home/ubuntu/discord_bot/elo_graphs/{}.png".format(username), 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)

    if '=online' == message.content.lower():
        
        the_message = await message.channel.send("please wait...")
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

    if message.content.startswith('=add') or message.content.startswith('=onlineadd'):

        themessage = message.content.lower()
        jg = valorant_online.addPlayer(themessage)

        if jg == False:
            await message.channel.send("Player does not exist")
        elif jg == True:
            await message.channel.send("Player has already been added")
        else:
            await message.channel.send("Player added")

    if message.content.startswith('=remove') or message.content.startswith('=onlineremove'):

        if message.author.id == 410771947522359296:
            themessage = message.content.lower()

            if valorant_online.removePlayer(themessage) == False:
                await message.channel.send("Player not in list")

            else:
                await message.channel.send("Player removed")
                
        else:
            await message.channel.send("no.")

    if message.content.startswith('=free'):

        themessage = message.content.lower()[6:]
        jg = themessage[0:5]
        week = schedule.Week(f'{jg}.csv')
        week.load()
        week.freetime(themessage[6:])
        week.save()
        await message.channel.send("Week updated.")

    if message.content.startswith('=busy'):

        themessage = message.content.lower()[6:]
        jg = themessage[0:5]
        week = schedule.Week(f'{jg}.csv')
        week.load()
        week.busy(themessage[6:])
        week.save()
        await message.channel.send("Week updated.")

    if message.content.startswith('=times'):

        week = schedule.Week(f'{message.content.lower()[7:]}.csv')
        week.load()
        jg = week.bestTimes()
        await message.channel.send("```\n" + jg + "\n```")

    if message.content.startswith('=clear'):

        if message.author.id == 410771947522359296:
            jg = message.content.lower()[7:]
            week = schedule.Week(f'{jg}.csv')
            week.load()
            week.clearWeek()
            week.save()
            await message.channel.send("Week reset.")
                
        else:
            await message.channel.send("no.")

    if message.content.startswith('=show'):

        week = schedule.Week(f'{message.content.lower()[6:]}.csv')
        week.load()
        jg = week.showWeek()
        await message.channel.send("```\n" + jg + "\n```")

    if '=help' == message.content.lower():
    
        msg = """Commands:
$leaderboard -> returns an elo leaderboard (slow)
$graph -> returns a graph of the player's elo over time
$elolist -> returns the elo values used in the graph
$online -> returns the player who are online from the list
$add -> adds the player to the database for leaderboard/graph/elolist
$addonline -> adds the player to the database for $online\n
Usage:
$leaderboard
$graph username (not username#tag)
$elolist username (not username#tag)
$online
$add username#tag name (name field is optional, if left blank, it'll use your username as the name)
$addonline username#tag name (name field optional)\n
Note: Being added to the online requires you to add henrick#API as a friend, after adding yourself
using $addonline, you will hopefully be send a friend request (don't send the friend request yourself)"""

        await message.channel.send("```\n" + msg + "\n```")



token = get_config()

client.run(token)
