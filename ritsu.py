import discord
import os
import weather
import valorant
import valorant_online_beta
import configparser
import graphs

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['openweathermap']['api'], c['openweathermap']['city_id'], c['discord']['token2']

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

    if '=weather' in message.content.lower():
        john = weather.main()
        await message.channel.send("Feels like " + str(john['main']['feels_like']) + " degrees today")

    if '$leaderboard' in message.content.lower():
        john = valorant.elo_leaderboard()
        await message.channel.send("```\n" + john + "\n```")

    if '=online' in message.content.lower():
        
        the_message = await message.channel.send("please wait...")
        valorant_online_beta.get_all_data()
        john = valorant_online_beta.everything()
        msg = ""

        for i in range(0, len(john)):
            if john[i][0] == "no parties" or john[i][0] == "Players Online:" or john[i][0] == "All players offline":
                msg += john[i][0] + '\n'
            elif john[i][0] == "Parties:":
                msg += '\n' + john[i][0] + '\n'
            else:  
                msg += john[i][0] + ": " + john[i][1] + '\n'
        await the_message.edit(content="```\n" + msg + "\n```")


    if message.content.lower().startswith('=graph'):
        themessage = message.content.lower()
        username = themessage[6:].strip()
        graphs.make_graph(username)
        with open("/home/ubuntu/discord_bot/elo_graphs/{}.png".format(username), 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

    if message.content.startswith('=elolist'):
        themessage = message.content.lower()
        username = themessage[8:].strip()
        elolist = valorant.get_elolist(username)
        await message.channel.send("```\n" + elolist + "\n```")

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))

    if "john" in message.content.lower():
        await message.add_reaction("\u2705")

    if message.content.lower().startswith('=test'):
        
        reply = message.content.lower()

        await message.channel.send(reply)    


config = get_config()
token = config[2]

client.run(token)
