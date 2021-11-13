import discord
from discord.ext import commands
import configparser
import valorant
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

def get_config():
    c = configparser.ConfigParser()
    c.read('config.ini')

    return c['discord']['ritsu']

token = get_config()

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='j',help_command = help_command)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [731539222141468673]

@client.event
async def on_ready():
    print("it started working")

@slash.slash(description="Ranked statistics for all acts",
             guild_ids=guild_ids,
             options = [
             create_option(name="username", description="enter username (user#tag)", option_type=3, required=True)])
async def stats(ctx, username=""):

    the_message = await ctx.send("fetching stats...")
    username = username.split('#')

    if len(username) == 2:

        fields = valorant.stats(username[0].lower(), username[1].lower())
        data = fields[0]
        card = fields[1]
        embed=discord.Embed(title = "Competitive Statistics", description="", color=0x00f900)
        embed.set_author(name=username[0].lower(), url = "https://youtu.be/MtN1YnoL46Q", icon_url=card)

        for field in data:
            embed.add_field(name = field[0], value = field[1], inline = True)

        embed.set_footer(text = "unlucky")
        await the_message.edit(contents = "", embed = embed)
    
    else:
        tag = valorant.get_tag(username[0].lower())
        
        if tag != "Player not found.":
            fields = valorant.stats(username[0].lower(), tag)
            data = fields[0]
            card = fields[1]
            embed=discord.Embed(title = "Competitive Statistics", description="", color=0x00f900)
            embed.set_author(name=username[0].lower(), url = "https://youtu.be/MtN1YnoL46Q", icon_url=card)
            
            for field in data:
                embed.add_field(name = field[0], value = field[1], inline = True)

            await the_message.edit(contents = "", embed = embed)

        else:
            await the_message.edit(content="```\n" + "Player not found, check syntax: (username#tag)" + "\n```")



@client.event
async def on_message(message):

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)

client.run(token)
