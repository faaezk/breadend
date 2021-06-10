import discord
import os
import weather
import valorant
import valorant_online
import configparser

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
        await message.channel.send("please wait...")
        john = valorant_online.everything()
        #await message.channel.send("```\n" + john[0][0] + "\n```")
        msg = ""

        for i in range(0, len(john)):
            if john[i][0] == "no parties":
                msg += john[i][0] + '\n'
            else:  
                msg += john[i][0] + ": " + john[i][1] + '\n'

        await message.channel.send("```\n" + msg + "\n```")

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))

    if "john" in message.content.lower():
        await message.add_reaction("\u2705")


config = get_config()
token = config[2]

client.run(token)
