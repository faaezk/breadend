import discord
import configparser

def get_token():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['token3']

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'jg-gasp' == message.content:
        name = message.content[3:]
        with open("stickers/{}.png".format(name), 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

token = get_token()

client.run(token)
