import os
import math
import config
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import valorant, playerclass
from adjustText import adjust_text
from exceptionclass import NoneException

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
    with open(f'{config.get("HISTORY_FP")}/{puuid}.txt', 'r') as f:
        for line in f:
            y.append(int(line.split(',')[0].strip()))

    if len(y) == 2:
        raise NoneException
    
    y.pop(0)
    return range(1, len(y) + 1), y

def generate_ticks(puuid, num_games=0):
    
    x, y = get_mmr_list(puuid)
    if not x:
        return(False, 'not enough data')

    if num_games != 0:
        y = y[-num_games:]
        x = range(1, len(y) + 1)

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

def graph(puuid, num_games=0, update=True, acts=False):

    playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerlist.load()
    ign = playerlist.get_ign_by_puuid(puuid)

    if update:
        try:
            valorant.update_database(puuid=puuid)
        except Exception as E:
            raise E

    x, y, x_ticks, y_ticks, y_labels, y_range = generate_ticks(puuid, num_games)

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
        try:
            act_data = valorant.get_data('MMR_BY_PUUID', puuid=puuid)
        except Exception as E:
            raise E

        act_data = act_data['data']['by_season']
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
    
    fig.savefig(f'{config.get("GRAPHS_FP")}/{puuid}.png', bbox_inches="tight")
    plt.close(fig)

    return True

def multigraph(puuid_list: list, update=False):

    ymin = 10000
    ymax = 0
    most_games = 0
    x_values, y_values, fails = [], [], []

    playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerlist.load()
    player_list = []
    
    for puuid in puuid_list:
        ign = playerlist.get_ign_by_puuid(puuid)
        if not puuid or not os.path.isfile(f'{config.get("HISTORY_FP")}/{puuid}.txt'):
            fails.append((ign, "Player not in database"))
        else:
            player_list.append((puuid, ign))

    if len(player_list) == 0:
        return (False, fails)

    for player in player_list:
        if update:
            try:
                valorant.update_database(player[0])
            except Exception as E:
                fails.append((player[1], E.message))
                continue
        
        try:
            x, y = get_mmr_list(player[0])
        except Exception as E:
            fails.append((player[1], E.message))

        x_values.append(x)
        y_values.append(y)

        if (rounddown(min(y)) < ymin):
            ymin = rounddown(min(y))
        
        if (roundup(max(y)) > ymax):
            ymax = roundup(max(y))

        if (len(y) > most_games):
            most_games = len(y)

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

    for i in range(len(player_list)):
        p = plt.plot(x_values[i], y_values[i], label=player_list[i][1])
        colour = p[0].get_color()
        plt.axhline(y=y_values[i][-1], color=colour, linestyle='--')

    plt.xlabel("Games played")
    plt.ylabel("MMR")
    plt.title("change in MMR over time")
    plt.legend()
    plt.savefig(f'{config.get("GRAPHS_FP")}/multigraph.png', bbox_inches="tight")
    plt.close()

    if len(fails) == 0:
        return (True, "")
    else:
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

    data = []

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
    playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerlist.load()

    for player in playerlist:
        if player.active != 'False':
            print(graph(puuid=player.puuid, update=False))
    return