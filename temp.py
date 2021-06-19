import matplotlib.pyplot as plt
import os
import playerlist
import math

players = playerlist.players

def roundup(x):
    return int(math.ceil(x / 50.0)) * 50

def rounddown(x):
    return int(math.floor(x / 50.0)) * 50

def roundcheck(x):

    while x > 100:
        x -= 100

    return x

def make_graph(username):

    file1 = open('/Users/faaezkamal/GitKraken Stuff/discord_bot/elo_history/faqinator.txt', 'r')
    #y = [736, 719, 700, 676, 641, 669, 666, 686]
    y = [x.strip() for x in file1.readlines()]
    y.pop(0)

    x = []
    for i in range(0, len(y)):
        y[i] = int(y[i]) + 1
        x.append(i + 1)

    ymin = min(y) - 25
    ymax = max(y) + 25

    axes = plt.gca()
    axes.set_ylim([ymin,ymax])
    
    ticks = []
    i = rounddown(ymin)
    while i < roundup(ymax):
        ticks.append(i)
        i += 25

    axes.set_yticks(ticks)
    
    plt.plot(x, y)
    plt.xlabel('your mother')
    plt.ylabel('mmr')
    plt.title(username + '\'s elo but the x axis has no meaning cause i cbs')
    file1.close()
    plt.show()

    print(axes.get_yticks())

make_graph("john")