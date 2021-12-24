import discord
from discord.ext import commands
import configparser
from discord_slash import SlashCommand
import personClass
import csv

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

@client.event
async def on_message(message):

    file = open('peoplecodes.txt','r')
    anonIDs = file.readlines()
    file.close()

    for i in range(0, len(anonIDs)):
        anonIDs[i] = anonIDs[i].strip()

    dontlook = []
    with open("dontlook.csv", "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            dontlook.append(line[0].split(','))

    Faaez =     personClass.Person("faaez",     410771947522359296, anonIDs[0])
    faq =       personClass.Person("faq",       776365641576742932, anonIDs[1])
    Dhiluka =   personClass.Person("dhiluka",   305132419474784257, anonIDs[2])
    Rasindu =   personClass.Person("rasindu",   285341337899761673, anonIDs[3])
    Dylan =     personClass.Person("dylan",     236820135254425600, anonIDs[4])
    Josh =      personClass.Person("josh",      389600778651959296, anonIDs[5])
    Vivian =    personClass.Person("vivian",    261818489159811072, anonIDs[6])
    Ethan =     personClass.Person("ethan",     400499749263769600, anonIDs[7])
    Albert =    personClass.Person("albert",    284881791335006209, anonIDs[8])
    Henry =     personClass.Person("henry",     290323655437713419, anonIDs[9])
    Joseph =    personClass.Person("joseph",    219270614362488832, anonIDs[10])
    Darren =    personClass.Person("darren",    286762644067713035, anonIDs[11])
    Delwyn =    personClass.Person("delwyn",    389687347605798913, anonIDs[12])
    Hadi =      personClass.Person("hadi",      251576622698856449, anonIDs[13])
    Will =      personClass.Person("will",      409908597397389313, anonIDs[14])
    Chris =     personClass.Person("chris",     320792211174195210, anonIDs[15])

    receiver = None
    people = [Faaez, faq, Rasindu, Dhiluka, Dylan, Josh, Vivian, Ethan, Albert, Henry, Joseph, Darren, Delwyn, Hadi, Will, Chris]

    if message.guild is None and not message.author.bot:
        print(message.content)

        name = message.content.split(' ')[0]
        words = message.content.replace(name, '')

        if name.lower() == 'reply':
            anonReceiverID = message.content.split(' ')[1]
            words = message.content.replace(name, '')
            words = words.replace(anonReceiverID, '')

            for person in people:
                if int(person.anonID) == int(anonReceiverID):
                    receiver = person
                    break
            
            if receiver == None:
                await message.author.send("invalid ID")

            else:
                flag = False
                for i in range(0, len(dontlook)):
                    if message.author.id == int(dontlook[i][0]):
                        if int(dontlook[i][2]) < 4:
                            dontlook[i][2] = int(dontlook[i][2]) + 1
                            flag = True
                            break

                if flag:
                    receiverUser = await client.fetch_user(receiver.discordID)
                    await receiverUser.send("reply: \n" + words.strip())
                    await message.author.send("message sent")
                
                else:
                    await message.author.send("message limit reached")

        else:
            for person in people:
                if person.discordID == message.author.id:
                    sender = person
                    break

            for person in people:
                if person.name == name:
                    receiver = person
                    break
            
            if receiver == None:
                await message.author.send("incorrect format, please provide name")
            
            else:
                flag = False
                for i in range(0, len(dontlook)):
                    if dontlook[i][0] == str(sender.discordID):
                        if dontlook[i][1] == '0':
                            dontlook[i][1] = str(receiver.anonID)
                            dontlook[i][2] = int(dontlook[i][2]) + 1
                            flag = True
                        else:
                            if dontlook[i][1] == str(receiver.anonID) and int(dontlook[i][2]) < 4:
                                dontlook[i][2] = int(dontlook[i][2]) + 1
                                flag = True
                        break

                if flag:
                    receiverUser = await client.fetch_user(receiver.discordID)
                    await receiverUser.send(words.strip() + '\nfrom: ' + str(sender.anonID)) 
                    await message.author.send("message sent")
                else:
                    await message.author.send("you cant send a message to that person or message limit reached")

        csvfile = open('dontlook.csv', 'w')
        for line in dontlook:
            csvfile.write(str(line[0]) + ',' + str(line[1]) + ',' + str(line[2]) + '\n')
        csvfile.close()

    await client.process_commands(message)

client.run(token)