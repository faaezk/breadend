import discord
from discord.ext import commands
import configparser
import malsearch
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/discord_bot/config.ini')

    return c['discord']['kenma']

token = get_config()

client = commands.Bot(command_prefix='!')
slash = SlashCommand(client, sync_commands=True)
guild_ids = [731539222141468673]

@client.event
async def on_ready():
    print("it started working")


@slash.slash(description="search MAL database",
             guild_ids=guild_ids,
             options = [create_option(name="title", description="Enter an anime to search for", option_type=3, required=False),
             create_option(name="character", description="Enter an character to search for", option_type=3, required=False),
             create_option(name="stats", description="Enter an anime to get stats for", option_type=3, required=False)])
async def anime(ctx, *, title = "", character = "", stats = ""):
    
    if title != "":
        await ctx.send("Getting info for " + title)
        anime = malsearch.animeSearch(title)

        if anime == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif anime == None:
            await ctx.send("Character not found.")

        else:
            embed = discord.Embed(title="{} ({})".format(anime['eng_title'], anime['jap_title']), url=anime['url'], 
            description="Source: {}, Type: {}, Score: {}, Episodes: {}".format(anime['source'], anime['type'], anime['score'], anime["ep_count"]))

            embed.set_image(url=anime['image_url'])
            embed.add_field(name="Airing Dates:", value=anime["Airing_Dates"])
            embed.add_field(name="Genres:", value=anime["genres"])
            embed.add_field(name="Sequel", value=anime["sequel"])
            embed.add_field(name="Opening Theme", value=anime["opening_themes"], inline=False)
            embed.add_field(name="Ending Theme", value=anime["ending_themes"], inline=False)
            embed.set_footer(text="Studios: {}, Licensors: {}".format(anime["studios"], anime["licensors"]))
            await ctx.send(embed=embed)

    elif character != "":
        await ctx.send("Getting info for " + character)
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
            
            await ctx.send(embed=embed)

    elif stats != "":
        await ctx.send("Getting stats for " + stats)
        anime = malsearch.animeStats(stats)

        if anime == False:
            await ctx.send("dumb dumb api failed, try again.")
        
        elif anime == None:
            await ctx.send("Character not found.")

        else:
            file=discord.File(fp="/home/ubuntu/discord_bot/image.png", filename='image.png')
            embed = discord.Embed(title=anime['title'], url=anime['url'])

            embed.set_image(url="attachment://image.png")

            embed.add_field(name="Other stats:", 
            value="Completed: {}\nWatching: {}\nPlan to watch: {}\nDropped: {}\nOn Hold: {}\nTotal: {}".format(
                anime["completed"], anime["watching"], anime["plan_to_watch"], anime["dropped"],
                anime["on_hold"], anime["total"]),
            inline=False)
            
            await ctx.send(file=file, embed=embed)

client.run(token)