import json
import random
import graphs
import config
import discord
import valorant
import requests
import malsearch
import playerclass

from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='$',help_command = help_command, intents=intents)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [config.TNG_GUILD_ID, config.TESTING_GUILD_ID]

@client.event
async def on_ready():
    print("it started working")

@slash.slash(description="Choices for Valorant",
             guild_ids=guild_ids,
             options = [
             create_option(name="randomise", description="returns random thing", option_type=3, required=False, 
                        choices=[create_choice(name="account",value="account"), create_choice(name="gamemode",value="gamemode"),
                        create_choice(name="weapon",value="weapon"), create_choice(name="agent",value="agent"),
                        create_choice(name="map",value="map")]),
             create_option(name="tactic", description="returns the plays for this round", option_type=3, required=False, 
                        choices=[create_choice(name="attacking",value="attacking"), create_choice(name="defending",value="defending")])])
async def choice(ctx, randomise="", tactic=""):
    
    if randomise == "account":
        await ctx.send(random.choices(['Smurfs', 'Mains'], weights=[40, 60], k=1)[0])
    
    if randomise == "gamemode":
        await ctx.send(random.choice(['Unrated', 'Competitive']))

    if randomise == "weapon":
        sidearm = ["Classic", "Shorty", "Frenzy", "Ghost", "Sheriff"]
        SMG = ["Stinger", "Spectre"]
        Shotgun = ["Bucky"]
        Rifle = ["Bulldog", "Guardian", "Phantom", "Vandal"]
        Sniper = ["Marshal", "Operator"]
        MG = ["Ares", "Odin"]
        selected = random.choice([sidearm, SMG, Shotgun, Rifle, Sniper, MG])
        await ctx.send(random.choice(selected))
    
    if randomise == "agent":
        await ctx.send(random.choice(["Astra", "Breach", "Brimstone", "Chamber", "Cypher", "Jett", "Killjoy", "Kay/O",
                                     "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", "Viper", "Yoru"]))

    if randomise == "map":
        await ctx.send(random.choice(["Bind", "Haven", "Split", "Ascent", "Icebox", "Breeze"]))

    if tactic == "attacking":
        await ctx.send(random.choice(["Rush A", "Rush B", "Rush C", "Cowboy Time", "Hide in spawn", "Split push",
                                        "Odin go brrr", "just ff", "Camp in corners", "Snipers only", "Pistol Prodigy"]))
    if tactic == "defending":
        await ctx.send(random.choice(["Everyone on A", "Everyone on B", "Everyone on C", "Cowboy Time", "Hide in spawn till plant",
                                        "Odin go brrr", "just ff", "Camp in corners", "Snipers only", "Pistol Prodigy"]))

@client.command()
async def cat(ctx):

    url = "https://api.thecatapi.com/v1/images/search?format=json"
    payload={}
    files={}
    headers = {'Content-Type': 'application/json', 'x-api-key': config.CAT_KEY}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    embed = discord.Embed(title="cat")
    embed.set_image(url=json.loads(response.text)[0]['url'])
    await ctx.send(embed=embed)

@slash.slash(description="graph",
             guild_ids=guild_ids,
             options = [
             create_option(name="usernames", description="Enter username(s), seperate with commas for more than one", option_type=3, required=True),
             create_option(name="type", description="Select type of graph", option_type=3, required=False, 
             choices=[create_choice(name="Basic",value="basic"), create_choice(name="With Acts",value="acts")]),
             create_option(name="update", description="Force update to latest MMR", option_type=3, required=False, 
             choices=[create_choice(name="No",value="no"), create_choice(name="Yes",value="yes")])])
async def graph(ctx, usernames="", type="", update=""):
    
    users = usernames.split(',')
    for i in range(len(users)):
        users[i] = users[i].split('#')[0].lower().strip()

    updates = True if update == 'yes' else False
    acts = True if type == 'acts' else False

    if len(users) == 1:
        the_message = await ctx.send("please wait...")
        msg = ""

        flag = graphs.make_graph(ign=users[0], update=updates, acts=acts)
        if not flag[0]:
            await the_message.edit(content=flag[1])
        else:
            with open(f"mmr_graphs/{users[0]}.png", 'rb') as f:
                picture = discord.File(f)
                await the_message.edit(content= "", file=picture)
    else:
        the_message = await ctx.send("please wait...")
        flag = graphs.multigraph(users, updates)
        msg = ""
        for fail in flag[1]:
            msg += f'{fail[0]} - {fail[1]}\n'
        if not flag[0]:
            await the_message.edit(content=msg)
        else:
            with open("mmr_graphs/multigraph.png", 'rb') as f:
                picture = discord.File(f)
            
            await the_message.edit(content=msg, file=picture)

@slash.slash(description="Add player to database for leaderboard and stuff",
             guild_ids=guild_ids,
             options = [
             create_option(name="ign", description="enter in game name", option_type=3, required=True), 
             create_option(name="tag", description="enter tag", option_type=3, required=True)])
async def add(ctx, ign="", tag=""):
    the_message = await ctx.send("please wait...")
    msg = valorant.add_player(ign.lower(), tag.lower())
    await the_message.edit(content=msg)

@slash.slash(description="Remove player from list",
             guild_ids=guild_ids,
             options = [create_option(name="username", description="enter username", option_type=3, required=True)])
async def remove(ctx, username=""):

    if ctx.author.id == 410771947522359296:
        username = username.split('#')
        ign = username[0].lower()
        msg = valorant.remove_player(ign)
        await ctx.send(msg)
    else:
        await ctx.send("no.")

@slash.slash(description="Update priority in database",
             guild_ids=guild_ids,
             options = [create_option(name="username", description="enter username", option_type=3, required=True),
             create_option(name="priority", description="Select type of graph", option_type=3, required=True, 
             choices=[create_choice(name="1",value="1"), create_choice(name="2",value="2"), create_choice(name="3",value="3")])])
async def updatePriority(ctx, username="", priority=""):

    if ctx.author.id == 410771947522359296:
        username = username.split('#')
        ign = username[0].lower()
        playerList = playerclass.PlayerList(config.PLAYERLIST_PATH)
        playerList.load()

        found = playerList.change_priority(ign, int(priority))

        if found:
            await ctx.send(f"{ign}'s priority has been updated to {priority}")
        else:
            await ctx.send(f"{ign} not found in database")
    else:
        await ctx.send("no.")

@client.command()
async def gettag(ctx, *, user):
    ign = user.lower()
    tag = valorant.get_tag(ign)
    if not valorant.get_tag(ign):
        await ctx.send("Player not in database")
    else:
        await ctx.send(f'{user}#{tag}')

@slash.slash(description="Get players banner",
             guild_ids=guild_ids,
             options = [create_option(name="username", description="enter username (ign#tag)", option_type=3, required=True)])
async def banner(ctx, username=""):

    username = username.split('#')
    ign = username[0].lower()
    puuid = "None"
    if len(username) == 2:
        tag = username[1].lower()
    else:
        playerList = playerclass.PlayerList(config.PLAYERLIST_PATH)
        playerList.load()
        puuid = playerList.get_puuid_by_ign(ign)

    data = valorant.get_banner(ign=ign, tag=tag, puuid=puuid)

    if not data[0]:
        await ctx.send(data[1])    
    else:
        await ctx.send(file=discord.File(fp="stuff/banner.png", filename='stuff/banner.png'))

@slash.slash(description="Update database with your new in-game name",
             guild_ids=guild_ids,
             options = [
             create_option(name="old_ign", description="enter your old ign", option_type=3, required=True),
             create_option(name="old_tag", description="enter your old tag", option_type=3, required=True),
             create_option(name="new_ign", description="enter your new ign", option_type=3, required=True),
             create_option(name="new_tag", description="enter your new tag", option_type=3, required=True)])
async def namechange(ctx, old_ign="", old_tag="", new_ign="", new_tag=""):

    if ctx.author.id == 410771947522359296:
        the_message = await ctx.send("please wait...")

        playerList = playerclass.PlayerList(config.PLAYERLIST_PATH)
        playerList.load()
        puuid = playerList.get_puuid_by_ign(old_ign)

        if puuid == "None":
            await the_message.edit(content = f'{old_ign}#{old_tag} not found in database')
        else:
            check = valorant.get_data('account', ign=new_ign, tag=new_tag)
            if not check[0]:
                await the_message.edit(content = f'{new_ign}#{new_tag} does not exist.')
            
            else:
                if playerList.change_ign(old_ign, new_ign, new_tag):
                    await the_message.edit(content = f'{old_ign}#{old_tag} is now {new_ign}#{new_tag}')
                else:
                    await the_message.edit(content = "something went wrong")            
    else:
        await ctx.send("no.")

@client.command()
async def getcsv(ctx):

    playerList = playerclass.PlayerList(config.PLAYERLIST_PATH)
    playerList.load()
    msg = ""

    for player in playerList.players:
        msg += str(player) + '\n'

    await ctx.send(content="```\n" + msg + "\n```")

@slash.slash(description="Valorant Servers Status", guild_ids=guild_ids)
async def serverstatus(ctx):
    the_message = await ctx.send("fetching statuses")
    await the_message.edit(content = valorant.servercheck())

@slash.slash(description="Lineup thing",
             guild_ids=guild_ids,
             options = [
             create_option(name="agent", description="Select agent to show lineup for", option_type=3, required=True, 
                        choices=[create_choice(name="Viper",value="viper")]),
             create_option(name="map", description="Select map to show lineup for", option_type=3, required=True, 
                        choices=[create_choice(name="Ascent",value="ascent")])])
async def lineup(ctx, agent="", map=""):

    if agent != "" and map != "":
        await ctx.send(f'https://atomic-potatos.github.io/Valorant-Lineups/agents/{agent}/{map}.html')

@slash.slash(description="Gives a crosshair", guild_ids=guild_ids)
async def crosshair(ctx):

    name, code = valorant.random_crosshair()
    if name:
        file=discord.File(fp="stuff/crosshair.png", filename='stuff/crosshair.png')
        embed = discord.Embed(title=name)
        embed.add_field(name="Code:", value=code)
        embed.set_image(url="attachment://stuff/crosshair.png")
        await ctx.send(content="", file=file, embed=embed)
    else:
        await ctx.send("the thingo failed.")

@slash.slash(description="List of other Commands", guild_ids=guild_ids)
async def other(ctx):
    msg = "```List of other commands:\n"
    msg += "$banner ign#tag -> returns your current banner\n"
    msg += "$cat -> returns a random cat photo\n"
    msg += "$getcsv -> returns playerlist\n"
    msg += "$gettag ign -> returns full username if they're in playerlist)```"
    await ctx.send(msg)

@slash.slash(description="search MAL database",
             guild_ids=guild_ids,
             options = [create_option(name="anime_title", description="Enter an anime to search for", option_type=3, required=False),
             create_option(name="manga_title", description="Enter an manga to search for", option_type=3, required=False),
             create_option(name="character", description="Enter a character to search for", option_type=3, required=False),
             create_option(name="anime_stats", description="Enter an anime to get stats for", option_type=3, required=False),
             create_option(name="manga_stats", description="Enter an manga to get stats for", option_type=3, required=False)])
async def MAL(ctx, *, anime_title = "", manga_title = "", character = "", anime_stats = "", manga_stats = ""):
    
    if anime_title != "":
        msg = await ctx.send("Getting info for " + anime_title)
        anime = malsearch.animeSearch(anime_title)

        if anime == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif anime == None:
            await ctx.send("Anime not found.")

        else:
            embed = discord.Embed(title="{} ({})".format(anime['eng_title'], anime['jap_title']), url=anime['url'], 
            description="Source: {}, Type: {}, Score: {}, Episodes: {}".format(anime['source'], anime['type'], anime['score'], anime["ep_count"]))

            embed.set_image(url=anime['image_url'])
            embed.add_field(name="Airing Dates:", value=anime["Airing_Dates"])
            embed.add_field(name="Genres:", value=anime["genres"])
            embed.add_field(name="Sequel", value=anime["sequel"])
            embed.add_field(name="Synopsis:", value=anime["synopsis"])
            embed.add_field(name="Opening Theme", value=anime["opening_themes"], inline=False)
            embed.add_field(name="Ending Theme", value=anime["ending_themes"], inline=False)
            embed.set_footer(text="Studios: {}, Licensors: {}".format(anime["studios"], anime["licensors"]))
            await msg.edit(content="", embed=embed)

    if manga_title != "":
        msg = await ctx.send("Getting info for " + manga_title)
        manga = malsearch.mangaSearch(manga_title)

        if manga == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif manga == None:
            await ctx.send("Manga not found.")

        else:
            embed = discord.Embed(title="{} ({})".format(manga['eng_title'], manga['jap_title']), url=manga['url'], 
            description="Type: {}, Score: {}, Volumes: {}, Chapters: {}".format(manga['type'], manga['score'], manga["vol_count"], manga["chap_count"]))

            embed.set_image(url=manga['image_url'])
            embed.add_field(name="Publishing Dates:", value=manga["publishing"])
            embed.add_field(name="Genres:", value=manga["genres"])
            embed.add_field(name="Authors:", value=manga["authors"])
            embed.add_field(name="Synopsis:", value=manga["synopsis"])
            embed.set_footer(text="Serialisations: {}".format(manga["serialisations"]))
            await msg.edit(content="", embed=embed)

    if character != "":
        msg = await ctx.send("Getting info for " + character)
        character = malsearch.characterSearch(character)

        if character == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif character == None:
            await ctx.send("Character not found.")

        else:
            embed = discord.Embed(title=character['name'], url=character['url'],
                                    description="Member favourites: " + str(character['member_favourites']))

            embed.set_image(url=character['image_url'])
            embed.add_field(name="Description", value=character["description"], inline=False)
            embed.add_field(name="Anime:", value=character["anime"], inline=False)
            embed.add_field(name="Manga:", value=character["manga"], inline=False)
            embed.add_field(name="Voice Actors:", value=character["voice_actors"], inline=False)
            
            await msg.edit(content="", embed=embed)

    if anime_stats != "":
        msg = await ctx.send("Getting stats for " + anime_stats)
        anime = malsearch.animeStats(anime_stats)

        if anime == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif anime == None:
            await ctx.send("Character not found.")

        else:
            file=discord.File(fp="stats.png", filename='stats.png')
            embed = discord.Embed(title=anime['title'], url=anime['url'])

            embed.set_image(url="attachment://stats.png")

            embed.add_field(name="Other stats:", 
            value="Completed: {}\nWatching: {}\nPlan to watch: {}\nDropped: {}\nOn Hold: {}\nTotal: {}".format(
                anime["completed"], anime["watching"], anime["plan_to_watch"], anime["dropped"],
                anime["on_hold"], anime["total"]),
            inline=False)
            
            await msg.edit(content="", file=file, embed=embed)

    if manga_stats != "":
        msg = await ctx.send("Getting stats for " + manga_stats)
        manga = malsearch.mangaStats(manga_stats)

        if manga == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif manga == None:
            await ctx.send("Character not found.")

        else:
            file=discord.File(fp="stuff/stats.png", filename='stuff/stats.png')
            embed = discord.Embed(title=manga['title'], url=manga['url'])

            embed.set_image(url="attachment://stuff/stats.png")

            embed.add_field(name="Other stats:", 
            value="Completed: {}\nReading: {}\nPlan to read: {}\nDropped: {}\nOn Hold: {}\nTotal: {}".format(
                manga["completed"], manga["reading"], manga["plan_to_read"], manga["dropped"],
                manga["on_hold"], manga["total"]),
            inline=False)
            
            await msg.edit(content="", file=file, embed=embed)

@slash.slash(description="rickies",
             guild_ids=guild_ids,)
async def chairmen(ctx):
    
    msg = await ctx.send("Getting info")
    url = "https://rickies.co/api/chairmen.json"

    headers = {'accept': 'application/json'}
    r = requests.get(url, headers=headers)
    chairmen = json.loads(r.text)

    keynote = chairmen['keynote_chairman']
    annual = chairmen['annual_chairman']


    embed = discord.Embed(title="The Rickies Chairmen", url="https://rickies.co/")

    #embed.set_image(url=chairmen['keynote_chairman']['memoji'])
    embed.add_field(name="Keynote Chairman:", value='{} {}'.format(keynote['name'], keynote['last_name']))
    embed.add_field(name="Keynote Chairman:", value='{} {}'.format(annual['name'], annual['last_name']))


    await msg.edit(content="", embed=embed)
    
@client.event
async def on_message(message):
                    
    if message.author == client.user:
        return

    if message.content.lower().startswith('good evening'):
        await message.channel.send(file=discord.File('stuff/good_evening.mp4'))
    
    if "wow" in message.content.lower() and message.author.id == 897988862658367549:
        await message.add_reaction("<:stevens:785800069957943306>")

    if message.content.lower().startswith('$lastupdate'):
        with open("updater_log-2023.out",'r') as f:
            for lastLine in f:
                pass

        await message.channel.send(lastLine)

    await client.process_commands(message)

client.run(config.POPO_TOKEN)