import discord
from discord.ext import commands
import configparser
import valorant
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


@slash.slash(description="Valorant Leaderboards",
             guild_ids=guild_ids,
             options = [
             create_option(name="options", description="Region/options for leaderboard (leave blank for local)", option_type=3, required=False, 
                        choices=[create_choice(name="Update local leaderboard",value="update"), create_choice(name="Asia Pacific",value="ap"),
                        create_choice(name="Europe",value="eu"), create_choice(name="Korea",value="kr"),
                        create_choice(name="North America",value="na")])])

async def choice(ctx, options=""):
    
    if options == "":
        john = "this is like, potentially up to 13 minutes old\n"
        f = open("leaderboard.txt", "r")
        for x in f:
            john += x
        f.close()

        await ctx.send("```\n" + john + "\n```")
    
    if options == "update":
        the_message = await ctx.send("this is gonna take a while...")
        john = valorant.elo_leaderboard()
        await the_message.edit(content="```\n" + john + "\n```")

    if options == "AP" or options == "EU" or options == "KR" or options == "NA":
        
        rleaderboard = valorant.region_leaderboard(options)

        if rleaderboard:
            contents = f'{options} Ranked Leaderboard\n'
            contents += rleaderboard
            await ctx.send("```\n" + contents + "\n```")
        
        else:
            await ctx.send("invalid region. select from: AP, NA, EU, KR")


@client.event
async def on_message(message):

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)

client.run(token)
