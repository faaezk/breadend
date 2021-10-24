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

@slash.slash(description="graph",
             guild_ids=guild_ids,
             options = [
             create_option(name="usernames", description="Enter username(s), seperate with commas for more than one", option_type=3, required=True)])
async def graph(ctx, usernames=""):
    users = usernames.split(',')
    
    for i in range(0, len(users)):
        users[i] = users[i].split('#')[0].lower().strip()

    if len(users) == 1:
        flag = graphs.make_graph(users[0])
        if flag == False:
            await ctx.send("Player not found")

        elif flag == None:
            await ctx.send("Not enough data to plot graph")

        else:
            with open(f"/home/ubuntu/discord_bot/elo_graphs/{users[0]}.png", 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)

    else:
        the_message = await ctx.send("please wait...")
        flag = graphs.multigraph(users)
        
        if flag == False:
            await the_message.edit("Player not found")

        elif flag == None:
            await the_message.edit("Not enough data to plot graph")

        else:
            with open("/home/ubuntu/discord_bot/elo_graphs/multigraph.png", 'rb') as f:
                picture = discord.File(f)
                await the_message.edit(content="", file=picture)
    


@client.event
async def on_message(message):

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))
    
    await client.process_commands(message)

client.run(token)
