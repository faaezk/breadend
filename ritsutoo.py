import discord
from discord.ext import commands
import configparser
import malsearch
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

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

@slash.slash(description="pong ping.")
async def pong(ctx):
    await ctx.send("ping")


@slash.slash(description="search MAL database",
             guild_ids=guild_ids,
             options = [create_option(name="title", description="Enter an anime to search for", option_type=3, required=False),
             create_option(name="character", description="Enter an character to search for", option_type=3, required=False)])
async def anime(ctx, *, title = "", character = ""):
    
    if title != "":
      await ctx.send("Getting info for " + title)
      anime = anime.animeSearch(title)

      embed = discord.Embed(title="{} ({})".format(anime['title_english'], anime['title_japanese']), url=anime['url'], 
                          description="Source: {}, Type: {}, Score: {}, Episodes: {}".format(anime['source'], anime['type'], anime['score'], ep_count))
      
      embed.set_image(url=anime['image_url'])
      embed.add_field(name="Airing Dates:", value=anime['aired']['string'])
      embed.add_field(name="Genres:", value=genres)
      embed.add_field(name="Sequel", value=sequel)
      embed.add_field(name="Opening Theme", value=opening_themes, inline=False)
      embed.add_field(name="Ending Theme", value=ending_themes, inline=False)
      embed.set_footer(text="Studios: {}, Licensors: {}".format(studios, licensors))
      await ctx.send(embed=embed)

    else:
      await ctx.send("it dont work")

client.run(token)