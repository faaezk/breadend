import discord
from discord.ext import commands
import configparser
import valorant
import graphs
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

def get_config():
    c = configparser.ConfigParser()
    c.read('config.ini')

    return c['discord']['ritsu']

token = get_config()

help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='!',help_command = help_command)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [731539222141468673]

@client.event
async def on_ready():
    print("it started working")

@slash.slash(description="graph",
             guild_ids=guild_ids,
             options = [
             create_option(name="usernames", description="Enter username(s), seperate with commas for more than one", option_type=3, required=True)])
async def newgraph(ctx, usernames=""):
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
        msg = ""
        if len(flag[0]) > 0:
            msg = "Players not found: "
            for elem in flag[0]:
                msg += elem + ", "
            msg = msg[:-2]

        if len(flag[1]) > 0:
            msg += '\n Players with not enough data to plot graph: '
            for elem in flag[1]:
                msg += elem + ", "
            msg = msg[:-2]

        if msg == "":
            with open("/home/ubuntu/discord_bot/elo_graphs/multigraph.png", 'rb') as f:
                picture = discord.File(f)
                await the_message.edit(content="", file=picture)
        
        else:
            await the_message.edit(content=msg)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))

    await client.process_commands(message)


client.run(token)