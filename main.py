import discord
import os
import weather
import configparser

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

config = get_config()
token = config[2]

client.run(token)