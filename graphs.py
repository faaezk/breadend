import matplotlib.pyplot as plt
import os
import valorant
import playerlist
import math

players = playerlist.players
ranks = {
0 : "Iron 1", 100 : "Iron 2", 200 : "Iron 3",
300 : "Bronze 1", 400 : "Bronze 2", 500 : "Bronze 3",
600 : "Silver 1", 700 : "Silver 2", 800 : "Silver 3",
900 : "Gold 1", 1000 : "Gold 2", 1100 : "Gold 3",
1200 : "Platinum 1", 1300 : "Platinum 2", 1400 : "Platinum 3",
1500 : "Diamond 1", 1600 : "Diamond 2", 1700 : "Diamond 3",
1800 : "Immortal"
}

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def rounddown(x):
    return int(math.floor(x / 100.0)) * 100

def make_graph(username):

    if os.path.isfile('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username)) == False:
        return
    
    tagline = ""
    for player in players:
        if player[0] == username:
            tagline = player[1]
            
    valorant.update_elo_history(username, tagline)
    
    file1 = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), 'r')

    y = [x.strip() for x in file1.readlines()]
    y.pop(0)
    x = []

    for i in range(0, len(y)):
        y[i] = int(y[i])
        x.append(i + 1)

    ymin = rounddown(min(y))
    ymax = roundup(max(y))

    axes = plt.gca()
    axes.set_ylim([ymin,ymax])
    
    ticks = []
    i = int(math.floor(ymin / 50.0)) * 50

    while i <= int(math.ceil(ymax / 50.0)) * 50:
        ticks.append(i)
        i += 25

    axes.set_yticks(ticks)
    labely = []

    for value in ticks:
        if value % 100 != 0:
            labely.append(str(value))

        else:
            labely.append(ranks[value])
    
    axes.set_yticklabels(labely)

    plt.plot(x, y)
    plt.xlabel('your mother')
    plt.ylabel('mmr')
    plt.title(username + '\'s elo but the x axis has no meaning cause i cbs')

    plt.savefig('/home/ubuntu/discord_bot/elo_graphs/{}.png'.format(username), bbox_inches="tight")

    file1.close()
    plt.clf()