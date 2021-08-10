import matplotlib.pyplot as plt
import os
import valorant
import playerclass
import math

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

def double_graph(user1, user2):

    if os.path.isfile('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(user1)) == False:
        return False
    
    if os.path.isfile('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(user2)) == False:
        return False
    
    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()

    tagline = ""
    for player in playerlist.players:
        if player.ign == user1:
            tagline = player.tag
            break

    valorant.update_elo_history(user1, tagline)

    tagline = ""
    for player in playerlist.players:
        if player.ign == user2:
            tagline = player.tag
            break

    valorant.update_elo_history(user2, tagline)
    
    file1 = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(user1), 'r')
    file2 = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(user2), 'r')

    y1 = [x.strip() for x in file1.readlines()]
    if len(y1) == 2:
        return None
    y1.pop(0)
    x1 = []

    for i in range(0, len(y1)):
        y1[i] = int(y1[i])
        x1.append(i + 1)

    y2 = [x.strip() for x in file2.readlines()]
    if len(y2) == 2:
        return None
    y2.pop(0)
    x2 = []

    for i in range(0, len(y2)):
        y2[i] = int(y2[i])
        x2.append(i + 1)


    if roundup(max(y1)) > roundup(max(y2)):
        ymax = roundup(max(y1))
    else:
        ymax = roundup(max(y2))
    
    if roundup(min(y1)) < roundup(min(y2)):
        ymin = roundup(min(y1))
    else:
        ymin = roundup(min(y2))


    axes = plt.gca()
    axes.set_ylim([ymin,ymax])
    
    ticks = []
    i = int(math.floor(ymin / 50.0)) * 50

    ranger = int((ymax-ymin)/100)

    while i <= int(math.ceil(ymax / 50.0)) * 50:
        ticks.append(i)
        if ranger == 1:
            i += 20
        elif ranger > 4:
            i += 50
        else:
            i += 25

    axes.set_yticks(ticks)
    labely = []

    for value in ticks:
        if value % 100 != 0:
            labely.append(str(value))

        else:
            labely.append(ranks[value])

    axes.set_yticklabels(labely)
    

    plt.plot(x1, y1, label = user1)
    plt.plot(x2, y2, label = user2)
    plt.xlabel('Games played')
    plt.ylabel('MMR')
    plt.title(f'{user1}\'s and {user2}\'s MMR over time')

    plt.savefig(f'/home/ubuntu/discord_bot/double_graphs/{user1}_{user2}.png', bbox_inches="tight")

    file1.close()
    plt.clf()

    return True

if __name__ == "__main__":
    double_graph('faqinator', 'fakinator')