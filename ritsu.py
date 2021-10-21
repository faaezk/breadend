import discord
from discord.ext import commands
import configparser
import graphs
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

@client.command(
    help="Syntax: $graph username or $graph username#tag", 
    brief="Returns a graph of the player's elo over time")
async def graph(ctx, *, username):

    username = username.split('#')[0].lower()
    flag = graphs.make_graph(username)
    
    if flag == False:
        await ctx.send("Player not found")

    elif flag == None:
        await ctx.send("Not enough data to plot graph")

    else:
        with open("/home/ubuntu/discord_bot/elo_graphs/{}.png".format(username), 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)


@slash.slash(description="graph",
             guild_ids=guild_ids,
             options = [
             create_option(name="username(s)", description="Enter usernames, seperate with commas for more than one", option_type=3, required=True)])
async def leaderboard(ctx, options=""):
    
    users = options.split(',')

    for user in users:
        user.strip()
        user = user.split('#')[0].lower()
    
    print(users)



@client.event
async def on_message(message):

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)

client.run(token)
