import matplotlib.pyplot as plt
import os
import valorant
import playerclass
import math
import pandas as pd
import numpy as np
from adjustText import adjust_text

ranks = {
0 : "Iron 1", 100 : "Iron 2", 200 : "Iron 3",
300 : "Bronze 1", 400 : "Bronze 2", 500 : "Bronze 3",
600 : "Silver 1", 700 : "Silver 2", 800 : "Silver 3",
900 : "Gold 1", 1000 : "Gold 2", 1100 : "Gold 3",
1200 : "Platinum 1", 1300 : "Platinum 2", 1400 : "Platinum 3",
1500 : "Diamond 1", 1600 : "Diamond 2", 1700 : "Diamond 3",
1800 : "Ascendant 1", 1900 : "Ascendant 2", 2000 : "Ascendant 3",
2100 : "Immortal 1", 2200 : "Immortal 2", 2300 : "Immortal 3",
2400 : "Radiant"
}

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def rounddown(x):
    return int(math.floor(x / 100.0)) * 100

def get_mmr_list(puuid):
    y = []
    with open(f'mmr_history/{puuid}.txt', 'r') as f:
        for line in f:
            y.append(int(line.split(',')[0].strip()))

    if len(y) == 2:
        return False, False
    
    y.pop(0)
    return range(1, len(y) + 1), y

def generate_ticks(puuid):
    
    x, y = get_mmr_list(puuid)
    if not x:
        return(False, 'not enough data')

    y_min = rounddown(min(y))
    y_max = roundup(max(y))

    y_ticks = []
    i = math.floor(y_min / 50.0) * 50
    y_range_len = int((y_max-y_min)/100)

    while i <= math.ceil(y_max / 50.0) * 50:
        y_ticks.append(i)
        if y_range_len == 1:
            i += 20
        elif y_range_len < 4:
            i += 25
        elif y_range_len < 8:
            i += 50
        else:
            i += 100

    y_labels = []

    for value in y_ticks:
        if value in ranks.keys():
            y_labels.append(ranks[value])
        else:
            y_labels.append(str(value))

    x_ticks = []  
    i = 0
    jump = 0

    if len(x) <= 15:
        jump = 1
    elif len(x) < 30:
        jump = 2
    elif len(x) < 70:
        jump = 5
    elif len(x) < 150:
        jump = 10

    if len(x) < 150:
        while i <= len(x):
            x_ticks.append(i)
            i += jump
    
        if x[-1] not in x_ticks:
            if (x[-1] - x_ticks[-1]) < 4:
                x_ticks[-1] = x[-1]
            else:
                x_ticks.append(x[-1])
    else:
        x_ticks = False

    return  x, y, x_ticks, y_ticks, y_labels, [y_min,y_max]

def graph(puuid="None", ign="", update=True, acts=False):

    if puuid == "None" and ign == "":
        return (False, 'no ign or puuid given')

    if puuid == "None" and ign != "":
        playerlist = playerclass.PlayerList('playerlist.csv')
        playerlist.load()
        puuid = playerlist.get_puuid_by_ign(ign)

    if puuid != "None" and ign == "":
        playerlist = playerclass.PlayerList('playerlist.csv')
        playerlist.load()
        ign = playerlist.get_ign_by_puuid(puuid)

    if puuid == "None" or ign == "":
        return (False, 'player not in database')

    if update:
        thing = valorant.update_database(puuid=puuid)
        if thing[0] == False:
            return thing
    
    x, y, x_ticks, y_ticks, y_labels, y_range = generate_ticks(puuid)

    fig, ax = plt.subplots()
    axes = fig.gca()
    axes.set_ylim(y_range)

    axes.set_yticks(y_ticks)
    if x_ticks:
        axes.set_xticks(x_ticks)
    axes.set_yticklabels(y_labels)

    p = ax.plot(x, y)
    colour = p[0].get_color()
    plt.axhline(y=y[-1], color=colour, linestyle=':', label='Cuurent MMR')
    plt.axhline(y=max(y), color=colour, linestyle='--', label='peak MMR')
    ax.set(xlabel='Games played', ylabel='MMR')
    ax.set_title(ign + '\'s MMR over time')

    if acts:
        act_data = valorant.get_data('mmr', puuid=puuid)
        if not act_data[0]:
            return act_data
        
        act_data = act_data[1]['data']['by_season']
        act_games = []

        for act in act_data.keys():
            if 'error' not in act_data[act].keys():
                act_games.append((act, act_data[act]['number_of_games']))

        temp = len(x)
        i = 0
        colours = ['b', 'r', 'g', 'k', 'c', 'm', 'y', 'darkgreen', 'peru']
        while temp > 0:
            plt.axvline(temp, linestyle="dotted", color=colours[i], label=act_games[i][0])
            temp -= act_games[i][1]
            i += 1

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend(loc='lower right')
    
    fig.savefig(f'mmr_graphs/{puuid}.png', bbox_inches="tight")
    plt.close(fig)

    return (True, True)

def multigraph(players: list, update=False):

    ymin = 10000
    ymax = 0
    most_games = 0
    x_values, y_values, fails = [], [], []

    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()

    for ign in players:
        puuid = playerlist.get_puuid_by_ign(ign)
        if puuid == "None":
            fails.append((ign, "Player not in database"))
            continue

        if os.path.isfile(f'mmr_history/{puuid}.txt') == False:
            fails.append((ign, "Player not in database"))
            continue
        
        if update:
            flag = valorant.update_database(puuid)
            if not flag[0]:
                fails.append((ign, flag[1]))
                continue

        x, y = get_mmr_list(puuid)
        if not x:
            return(False, 'not enough data')

        x_values.append(x)
        y_values.append(y)

        if (rounddown(min(y)) < ymin):
            ymin = rounddown(min(y))
        
        if (roundup(max(y)) > ymax):
            ymax = roundup(max(y))

        if (len(y) > most_games):
            most_games = len(y)

    if len(fails) == len(players):
        return (False, fails)
    
    for failure in fails:
        players.remove(failure[0])

    axes = plt.gca()
    axes.set_ylim([ymin,ymax])
    
    y_ticks = []
    i = int(math.floor(ymin / 50.0)) * 50
    ranger = int((ymax-ymin)/100)

    while i <= int(math.ceil(ymax / 50.0)) * 50:
        y_ticks.append(i)
        if ranger == 1:
            i += 20
        elif ranger > 4:
            i += 50
        else:
            i += 25

    axes.set_yticks(y_ticks)
    y_labels = []

    for value in y_ticks:
        if value % 100 != 0:
            y_labels.append(str(value))
        else:
            y_labels.append(ranks[value])

    axes.set_yticklabels(y_labels)

    for i in range(len(players)):
        p = plt.plot(x_values[i], y_values[i], label=players[i])
        colour = p[0].get_color()
        plt.axhline(y=y_values[i][-1], color=colour, linestyle='--')

    plt.xlabel("Games played")
    plt.ylabel("MMR")
    plt.title("change in MMR over time")
    plt.legend()
    plt.savefig(f'mmr_graphs/multigraph.png', bbox_inches="tight")
    plt.close()

    return (True, fails)

def mark_graph(texts, x, yint, ydates, i, marked, r):
    if i < 0:
        i = len(yint) + i

    if i not in marked:
        texts.append(plt.text(s=ydates[i], x=x[i], y=yint[i], bbox=dict(boxstyle="round, pad=0.2", fc="cyan"), size=8.0))
        for j in range(i - r, i + r):
            if j >= 0 and j not in marked:
                if j == len(yint):
                    break
                marked.append(j)
    return marked, texts

def date_graph():

    months = {"January" : 1, "February" : 2, "March" : 3, 
            "April" : 4, "May" : 5, "June" : 6,
            "July" : 7, "August" : 8, "September" : 9, 
            "October" : 10, "November" : 11, "December" : 12}

    data = ["1724,Sunday-July-10-2022-7:42-AM", "1707,Sunday-July-10-2022-8:18-AM", "1700,Sunday-July-10-2022-9:14-AM", "1721,Sunday-July-10-2022-9:52-AM", 
        "1710,Sunday-July-10-2022-12:22-PM", "1723,Sunday-July-10-2022-1:07-PM", "1712,Sunday-July-10-2022-1:55-PM", "1700,Monday-July-11-2022-12:28-PM",
        "1720,Monday-July-11-2022-1:19-PM",  "1736,Monday-July-11-2022-2:08-PM", "1750,Monday-July-11-2022-2:54-PM", "1736,Monday-July-11-2022-4:52-PM", 
        "1755,Tuesday-July-12-2022-9:51-AM", "1741,Tuesday-July-12-2022-2:05-PM", "1755,Tuesday-July-12-2022-2:54-PM","1771,Tuesday-July-12-2022-3:59-PM",
        "1768,Tuesday-July-12-2022-4:44-PM", "1755,Tuesday-July-12-2022-4:48-PM", "1772,Wednesday-July-13-2022-7:41-AM", "1757,Wednesday-July-13-2022-8:28-AM", 
        "1774,Wednesday-July-13-2022-9:20-AM", "1796,Wednesday-July-13-2022-12:08-PM" ,"1816,Wednesday-July-13-2022-12:41-PM", "1801,Wednesday-July-13-2022-1:18-PM", 
        "1800,Wednesday-July-13-2022-4:35-PM", "1785,Thursday-July-14-2022-12:11-PM", "1810,Thursday-July-14-2022-12:58-PM", "1824,Thursday-July-14-2022-3:17-PM", 
        "1840,Thursday-July-14-2022-4:00-PM", "1861,Friday-July-15-2022-5:33-AM", "1843,Friday-July-15-2022-6:06-AM", "1862,Friday-July-15-2022-6:40-AM", 
        "1880,Friday-July-15-2022-10:00-AM", "1864,Friday-July-15-2022-12:08-PM", "1848,Friday-July-15-2022-12:50-PM", "1868,Saturday-July-16-2022-1:58-PM", 
        "1852,Saturday-July-16-2022-2:39-PM", "1840,Saturday-July-16-2022-3:38-PM", "1827,Saturday-July-16-2022-4:27-PM", 
        "1847,Sunday-July-17-2022-6:52-AM",  "1865,Sunday-July-17-2022-12:17-PM", "1847,Sunday-July-17-2022-1:14-PM", "1831,Sunday-July-17-2022-1:50-PM", 
        "1846,Sunday-July-17-2022-3:28-PM", "1832,Sunday-July-17-2022-4:07-PM", "1852,Monday-July-18-2022-1:05-PM", "1834,Tuesday-July-19-2022-4:53-AM", 
        "1854,Tuesday-July-19-2022-5:39-AM", "1837,Tuesday-July-19-2022-12:14-PM", "1823,Tuesday-July-19-2022-1:08-PM", "1808,Tuesday-July-19-2022-3:50-PM", 
        "1825,Tuesday-July-19-2022-4:23-PM", "1846,Wednesday-July-20-2022-6:14-AM", "1831,Wednesday-July-20-2022-6:52-AM", "1814,Wednesday-July-20-2022-7:38-AM", 
        "1800,Wednesday-July-20-2022-8:19-AM", "1819,Wednesday-July-20-2022-11:52-AM", "1802,Wednesday-July-20-2022-12:45-PM", "1822,Thursday-July-21-2022-2:17-PM",
        "1835,Thursday-July-21-2022-3:10-PM", "1817,Friday-July-22-2022-3:40-AM", "1838,Friday-July-22-2022-4:10-AM", "1822,Friday-July-22-2022-1:51-PM", 
        "1839,Friday-July-22-2022-2:25-PM", "1852,Friday-July-22-2022-2:53-PM", "1874,Saturday-July-23-2022-4:45-AM", "1892,Saturday-July-23-2022-5:40-AM", 
        "1875,Saturday-July-23-2022-6:39-AM", "1861,Saturday-July-23-2022-12:58-PM", "1881,Saturday-July-23-2022-1:54-PM", "1863,Saturday-July-23-2022-2:35-PM",
        "1850,Saturday-July-23-2022-3:48-PM", "1864,Saturday-July-23-2022-4:28-PM", "1886,Sunday-July-24-2022-5:39-AM", "1910,Sunday-July-24-2022-6:11-AM", 
        "1900,Sunday-July-24-2022-7:10-AM", "1884,Monday-July-25-2022-2:10-PM", "1910,Monday-July-25-2022-2:48-PM", "1900,Monday-July-25-2022-3:26-PM", 
        "1882,Monday-July-25-2022-4:02-PM", "1899,Tuesday-July-26-2022-12:28-PM", "1921,Tuesday-July-26-2022-1:50-PM", "1902,Tuesday-July-26-2022-2:24-PM", 
        "1914,Wednesday-July-27-2022-1:43-PM", "1928,Wednesday-July-27-2022-2:27-PM", "1910,Thursday-July-28-2022-4:40-AM", "1926,Thursday-July-28-2022-5:39-AM", 
        "1905,Thursday-July-28-2022-9:45-AM", "1924,Thursday-July-28-2022-2:33-PM", "1910,Thursday-July-28-2022-4:01-PM", "1900,Friday-July-29-2022-12:06-PM", 
        "1914,Friday-July-29-2022-1:47-PM", "1900,Friday-July-29-2022-2:23-PM", "1919,Saturday-July-30-2022-6:14-AM", "1940,Saturday-July-30-2022-7:03-AM", 
        "1917,Saturday-July-30-2022-7:36-AM", "1900,Saturday-July-30-2022-8:00-AM"]

    num_points = len(data)
    rows_list, years = [], []

    for i in range(num_points):
            temp = data[i].split(',')
            ts = temp[1].split('-')
            dict1 = {'x' : i + 1, 'MMR' : int(temp[0]), 'dates' : f"{ts[2]}/{months[ts[1]]}"}
            dict1.update()
            rows_list.append(dict1)

            added = False
            for year in years:
                if ts[3] == year[0]:
                    added = True
                    if (i + 1) > year[1]:
                        year[1] = (i + 1)
                
            if not added:
                years.append([ts[3], i])

    df = pd.DataFrame(rows_list)
    y_labels, y_ticks, x_ticks = [], [], []
    ymin = rounddown(min(df['MMR']) - 1) + 50
    ymax = roundup(max(df['MMR']) + 1) + 25
    i = int(math.floor((ymin) / 50.0)) * 50
    ranger = int((ymax - ymin)/100)

    while i <= int(math.ceil(ymax / 25.0)) * 25:
        y_ticks.append(i)
        if i % 100 == 0:
            y_labels.append(ranks[i])
        else:
            y_labels.append(str(i))

        if ranger == 1:
            i += 20
        elif ranger < 4:
            i += 25
        elif ranger < 8:
            i += 50
        else:
            i += 100

    axes = plt.gca()
    axes.set_ylim([ymin,ymax])
    axes.set_yticks(y_ticks)
    axes.set_yticklabels(y_labels)

    if num_points < 300:
        i = 0
        if num_points <= 15:
            j = 1
        elif num_points < 30:
            j = 2
        elif num_points < 70:
            j = 5
        elif num_points < 150:
            j = 10
        else:
            j = 20

        while i <= num_points:
            x_ticks.append(i)
            i += j

        if (num_points - 1) not in x_ticks:
            if ((num_points - 1) - x_ticks[-1]) < 5:
                x_ticks[-1] = (num_points - 1)
            else:
                x_ticks.append((num_points - 1))

        axes.set_xticks(x_ticks)

    p = plt.plot(df['x'], df['MMR'], 'b-')
    
    r = math.floor(num_points/7.0)
    minIndex = df.loc[df['MMR'] == min(df['MMR'])].index[0]
    maxIndex = df.loc[df['MMR'] == max(df['MMR'])].index[0]
    mark = [0, -1, minIndex, maxIndex]
    topRightTexts, botRightTexts, topLeftTexts, botLeftTexts = [], [], [], []

    diffed = np.diff(df['MMR'].to_numpy())

    print(diffed)
    
    for year in years:
        plt.axvline(year[1], linestyle="dotted", color="k", label=year[0])

    adjust_text(topRightTexts, arrowprops=dict(arrowstyle='->'), force_points=(20, 30), force_text=(30, 30))
    adjust_text(botRightTexts, arrowprops=dict(arrowstyle='->'), force_points=(20, -40), force_text=(30, 30))
    adjust_text(botLeftTexts, arrowprops=dict(arrowstyle='->'), force_points=(-70, -40), force_text=(30, 30))
    adjust_text(topLeftTexts, arrowprops=dict(arrowstyle='->'), force_points=(-70, 30), force_text=(30, 30))

    colour = p[0].get_color()
    plt.axhline(df['MMR'].iloc[num_points - 1], linestyle="dashed", color=colour, label='Current MMR')
    plt.xlabel('Games played')
    plt.ylabel('MMR')
    plt.title('MMR over tifme')
    plt.legend(loc='upper left')
    plt.savefig('stuff/date-graph.png', bbox_inches="tight")

def update_all_graphs():
    playerlist = playerclass.PlayerList('playerlist.csv')
    playerlist.load()

    for i in range(len(playerlist.players)):
        if playerlist.players[i].active != 'False':
            print(graph(puuid=playerlist.players[i].puuid, update=False))
    return

if __name__ == "__main__":
    print(graph(ign='fakinator', update=True, acts=False))