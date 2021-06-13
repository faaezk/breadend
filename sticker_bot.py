import discord
import configparser
import os
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

    if message.content == '$stickerlist':
        files = os.listdir('/home/ubuntu/discord_bot/stickers')
        files.sort()
        msg = ""
        for file in files:
            msg += str(file[:-4]) + '\n'
        await message.channel.send("```\n" + msg + "```")

    if message.content.startswith('jg-'):
        name = message.content[3:]

        if os.path.isfile('stickers/{}.png'.format(name)) == False:
            await message.channel.send("not a sticker")
        else:
            with open("stickers/{}.png".format(name), 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
                await message.delete()

token = get_token()

client.run(token)
