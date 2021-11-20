import discord
from discord.ext import commands
import configparser
import newvalorant
import valorant
import elo_history_updater
import playerclass
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

@slash.slash(description="MMR history list",
             guild_ids=guild_ids,
             options = [
             create_option(name="username", description="enter username (ign#tag)", option_type=3, required=True)])
async def newelolist(ctx, username=""):
    
    username = username.split('#')[0].lower()
    elolist = newvalorant.get_elo_list(username)
    if elolist == None:
        await ctx.send("No comp games recorded")
    
    elif elolist == False:
        await ctx.send("Player not found")
    
    else:
        await ctx.send("```\n" + elolist + "\n```")

@slash.slash(description="Ranked statistics for all acts",
             guild_ids=guild_ids,
             options = [
             create_option(name="username", description="enter username (ign#tag)", option_type=3, required=True)])
async def newstats(ctx, username=""):

    the_message = await ctx.send("fetching stats...")
    username = username.split('#')

    ign = username[0].lower()

    if len(username) == 2:
        tag = username[1].lower()
    else:
        tag = ""

    fields = newvalorant.stats(ign, tag)

    if type(fields) == str:
        await the_message.edit(content=fields)
    
    else:
        data = fields[0]
        card = fields[1]
        embed=discord.Embed(title = "Competitive Statistics", description="", color=0x00f900)
        embed.set_author(name=ign, url = "https://youtu.be/MtN1YnoL46Q", icon_url=card)

        for field in data:
            embed.add_field(name = field[0], value = field[1], inline = True)

        await the_message.edit(contents = "", embed = embed)

@slash.slash(description="Valorant Leaderboards",
             guild_ids=guild_ids,
             options = [
             create_option(name="options", description="Region/options for leaderboard (leave blank for local)", option_type=3, required=False, 
                        choices=[create_choice(name="Update local leaderboard",value="update"), create_choice(name="Asia Pacific",value="ap"),
                        create_choice(name="Europe",value="eu"), create_choice(name="Korea",value="kr"),
                        create_choice(name="North America",value="na")])])
async def newleaderboard(ctx, options=""):
    
    if options == "":

        log_file = open("elo_history/run_check.out",'r')
        lines = log_file.readlines()
        log_file.close()

        leaderboard = "Last updated at " + lines[-1].split(' ')[4] +'\n'
        newvalorant.local_leaderboard()
        f = open("leaderboard.txt", 'r')
        for x in f:
            leaderboard += x
        f.close()

        await ctx.send("```\n" + leaderboard + "\n```")
    
    if options == "update":
        the_message = await ctx.send("this is gonna take a while...")
        elo_history_updater.update_all_elo_history()
        newvalorant.local_leaderboard()
        leaderboard = ""
        f = open("leaderboard.txt", "r")
        for x in f:
            leaderboard += x
        f.close()
        
        await the_message.edit(content="```\n" + leaderboard + "\n```")

    if options == "ap" or options == "eu" or options == "kr" or options == "na":
        
        the_message = await ctx.send("fetching leaderboard...")
        rleaderboard = newvalorant.region_leaderboard(options)

        if rleaderboard:
            await the_message.edit(content="```\n" + rleaderboard + "\n```")

@slash.slash(description="Add player to database for leaderboard and stuff",
             guild_ids=guild_ids,
             options = [
             create_option(name="username", description="enter username (ign#tag)", option_type=3, required=True)])
async def newadd(ctx, username=""):

    username = username.split('#')

    if len(username) == 2:
        the_message = await ctx.send("please wait...")
        msg = valorant.add_player(username[0].lower(), username[1].lower())
        await the_message.edit(contents=msg)

    else:
        await ctx.send("Player not found, check syntax: (ign#tag)")

@slash.slash(description="Remove player from list",
             guild_ids=guild_ids,
             options = [
             create_option(name="username", description="enter username (ign#tag)", option_type=3, required=True)])
async def newremove(ctx, username=""):

    if ctx.author.id == 410771947522359296:
        username = username.split('#')
        if len(username) == 2:
            msg = newvalorant.remove_player(username[0].lower(), username[1].lower())
            await ctx.send(msg)
        else:
            await ctx.send("Player not found, check syntax: (ign#tag)")
            
    else:
        await ctx.send("no.")

@client.command()
async def newgettag(ctx, *, ign):
    ign = ign.lower()
    if not newvalorant.get_tag(ign):
        await ctx.send("Player not in database. add using /add")
    else:
        await ctx.send(f'{ign}#{newvalorant.get_tag(ign)}')

@client.command()
async def banner(ctx, *, username):

    username = username.split('#')
    ign = username[0].lower()

    if len(username) == 2:
        tag = username[1].lower()
    else:
        tag = newvalorant.get_tag(ign)

    if not tag:
        await ctx.send("Player not found, check syntax: (ign#tag)")
    
    else:
        msg = newvalorant.get_banner(ign, tag)

        if type(msg) == str:
            await ctx.send(msg)
        
        else:
            await ctx.send(file=discord.File('banner.png'))

@slash.slash(description="Changing your in-game name",
             guild_ids=guild_ids,
             options = [
             create_option(name="old_username", description="enter your old username", option_type=3, required=True),
             create_option(name="new_username", description="enter your new username (user#tag)", option_type=3, required=True)])
async def newnamechange(ctx, old_username="", new_username=""):

    if ctx.author.id == 410771947522359296:

        old = old_username.split('#')[0].lower()
        new_username = new_username.split('#')

        if len(new_username) != 2:
            await ctx.send("check syntax: (ign#tag)")
        
        else:
            the_message = await ctx.send("please wait...")
            new_ign = new_username[0].lower()
            new_tag = new_username[1].lower()

            if valorant.account_check(new_ign, new_tag):
                playerList = playerclass.PlayerList('playerlist.csv')
                playerList.load()
                if playerList.change_ign(old, new_ign, new_tag):
                    playerList.save()
                    await the_message.edit(content = f'{old} is now {new_ign}#{new_tag}')
                
                else:
                    await the_message.edit(content = f'{old} not found in database, check player list using `$getcsv`')
            
            else:
                await the_message.edit(content = f'{new_ign}#{new_tag} does not exist.')

@slash.slash(description="Valorant Servers Status", guild_ids=guild_ids)
async def newserverstatus(ctx):
    the_message = await ctx.send("fetching statuses")
    await the_message.edit(content = newvalorant.servercheck())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('good_evening.mp4'))

    await client.process_commands(message)


client.run(token)