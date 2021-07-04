import discord
import weather
import configparser
import valorant_online
import graphs
import valorant
import temp

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['openweathermap']['api'], c['openweathermap']['city_id'], c['discord']['token']

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$heello'):
        await message.channel.send('Hello!')

    if '$weather' in message.content.lower():
        john = weather.main()
        await message.channel.send("Feels like " + str(john['main']['feels_like']) + " degrees today")

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))

    if "wow" in message.content.lower() and message.author.id == 203311457666990082:
        await message.add_reaction("<:stevens:785800069957943306>")

    if message.content.lower().startswith('$graph'):

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

    if message.content.startswith('$elolist'):

        themessage = message.content.lower()
        username = themessage[8:].strip()
        elolist = valorant.get_elolist(username)

        await message.channel.send("```\n" + elolist + "\n```")

    if message.content.lower().startswith('$leaderboard'):
        john = valorant.elo_leaderboard()
        await message.channel.send("```\n" + john + "\n```")
    
    if '$online' == message.content.lower():
        
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

    if message.content.startswith('$add') or message.content.startswith('$onlineadd'):

        themessage = message.content.lower()
        jg = temp.addPlayer(themessage)

        if jg == False:
            await message.channel.send("Player does not exist")
        elif jg == True:
            await message.channel.send("Player has already been added")
        else:
            await message.channel.send("Player added")

    if message.content.startswith('$remove') or message.content.startswith('$onlineremove'):

        if message.author.id == 410771947522359296:
            themessage = message.content.lower()

            if temp.removePlayer(themessage) == False:
                await message.channel.send("Player not in list")

            else:
                await message.channel.send("Player removed")
                
        else:
            await message.channel.send("no.")

    if '$valhelp' == message.content.lower():
    
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
using $addonline, you will hopefully be send a friend request (don't send the friend request yourself)
for any further questions, ask faaez"""

        await message.channel.send("```\n" + msg + "\n```")


config = get_config()
token = config[2]

client.run(token)