import matplotlib.pyplot as plt
import os
import elo_history
import playerlist

players = playerlist.players

def make_graph(username):

    if os.path.isfile('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username)) == False:
        return
    
    tagline = ""
    for player in players:
        if player[0] == username:
            tagline = player[1]
    elo_history.update_elo_history(username, tagline)
    
    file1 = open('/home/ubuntu/discord_bot/elo_history/{}.txt'.format(username), 'r')

    y = [x.strip() for x in file1.readlines()]
    y.pop(0)

    x = []
    for i in range(0, len(y)):
        y[i] = int(y[i])
        x.append(i)

    plt.plot(x, y)
    plt.xlabel('your mother')
    plt.ylabel('mmr')
    plt.title(username + '\'s elo but the x axis has no meaning cause i cbs')

    plt.savefig('/home/ubuntu/discord_bot/elo_graphs/{}.png'.format(username))
    file1.close()
    plt.clf()