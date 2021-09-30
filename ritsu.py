import discord
from discord.ext import commands
import configparser
import malsearch
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['ritsu']

token = get_config()

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='j',help_command = help_command)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [731539222141468673]

@client.event
async def on_ready():
    print("it started working")

@client.command()
async def g(ctx, message=None):

        member = message.author.name

        webhook = await ctx.channel.create_webhook(name=member.name)
        await webhook.send(
            str(message), username=member.name, avatar_url=member.avatar_url)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
                await webhook.delete()

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    user = client.get_user(message.author.id)

    print(user)
    print(message.author.display_name)

    if message.content.startswith('name'):
        
        member=message.author

        webhook = await message.channel.create_webhook(name=member.display_name)
        await webhook.send("changed name\n", username=member.display_name, avatar_url=member.avatar_url)

        webhooks = await message.channel.webhooks()
        for webhook in webhooks:
                await webhook.delete()



    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)

client.run(token)
