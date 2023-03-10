import discord
import configparser
from discord.ext import commands
import typing

def get_token():
	c = configparser.ConfigParser()
	c.read('config.ini')
	return c['discord']['ritsu']

token = get_token()
guild_id = 731539222141468673
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def pong(ctx, arg, arg2: typing.Optional[str] = 'no'):
	await ctx.send(arg + arg2)
	print('yes')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    await bot.process_commands(message)
		
bot.run(token)