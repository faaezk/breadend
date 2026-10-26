import os
import math
import hashlib
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from adjustText import adjust_text

import config
import valorant
import playerclass
from exceptionclass import NoneException, MissingException

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

DATE_FORMAT = "%A-%B-%d-%Y-%I:%M-%p"

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def rounddown(x):
    return int(math.floor(x / 100.0)) * 100

def get_mmr_list(puuid):
    # First line of the history file is the last-update timestamp
    with open(f"{config.get('MMR_HISTORY')}/{puuid}.txt", 'r') as f:
        lines = f.readlines()[1:]

    y = [int(line.split(',')[0].strip()) for line in lines if line.strip()]
    if len(y) < 2:
        raise NoneException

    return range(1, len(y) + 1), y

def get_dated_mmr_list(puuid):
    with open(f"{config.get('MMR_HISTORY')}/{puuid}.txt", 'r') as f:
        lines = f.readlines()[1:]

    dates, y = [], []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) < 2 or not parts[1]:
            continue
        dates.append(datetime.strptime(parts[1], DATE_FORMAT))
        y.append(int(parts[0]))

    if len(y) < 2:
        raise NoneException

    return dates, y

def generate_y_ticks(y_min, y_max):
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

    return y_ticks, [ranks.get(value, str(value)) for value in y_ticks]

def generate_ticks(puuid, num_games=0):
    x, y = get_mmr_list(puuid)

    if not x:
        raise NoneException

    if num_games != 0:
        y = y[-num_games:]
        x = range(1, len(y) + 1)

    y_min = rounddown(min(y))
    y_max = roundup(max(y))
    y_ticks, y_labels = generate_y_ticks(y_min, y_max)

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

def graph(puuid, num_games=0, update=False, acts=False):
    playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerlist.load()
    ign = playerlist.get_ign_by_puuid(puuid)

    if not ign:
        raise MissingException

    if update:
        valorant.update_database(puuid)

    x, y, x_ticks, y_ticks, y_labels, y_range = generate_ticks(puuid, num_games)

    fig = Figure()
    ax = fig.subplots()
    ax.set_ylim(y_range)

    ax.set_yticks(y_ticks)
    if x_ticks:
        ax.set_xticks(x_ticks)
    ax.set_yticklabels(y_labels)

    p = ax.plot(x, y)
    colour = p[0].get_color()
    ax.axhline(y=y[-1], color=colour, linestyle=':', label='Current MMR')
    ax.axhline(y=max(y), color=colour, linestyle='--', label='peak MMR')
    ax.set(xlabel='Games played', ylabel='MMR')
    ax.set_title(ign + '\'s MMR over time')

    if acts:
        act_data = valorant.get_data('MMR_BY_PUUID', puuid=puuid)
        act_data = act_data['data']['by_season']
        act_games = []

        for act in act_data.keys():
            title = act.replace("e", " Ep ")
            title = title.replace("a", ", Act ")
            if 'error' not in act_data[act].keys():
                act_games.append((title, act_data[act]['number_of_games']))

        temp = len(x)
        i = 0
        colours = ['lightcoral', 'chocolate',  'goldenrod',  'olive',  'turquoise',  
                   'indigo',  'red',  'peru',  'gold',  'greenyellow',  'teal',  
                   'violet',  'salmon',  'orange',  'khaki',  'lawngreen',  
                   'aqua',  'purple',  'orangered',  'yellow',  'palegreen',  
                   'skyblue',  'fuchsia',  'limegreen',  'blue',  'hotpink',  'lime']

        while temp > 0 and i < len(act_games):
            ax.axvline(temp, linestyle="dotted", color=colours[i % len(colours)], label=act_games[i][0])
            temp -= act_games[i][1]
            i += 1

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend(loc='lower right')
    
    fig.savefig(f"{config.get('MMR_GRAPH')}/{puuid}.png", bbox_inches="tight")

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
        if not puuid or not os.path.isfile(f"{config.get('MMR_HISTORY')}/{puuid}.txt"):
            fails.append((ign, "Player not in database"))
        else:
            player_list.append((puuid, ign))

    plotted = []
    for player in player_list:
        if update:
            try:
                valorant.update_database(player[0])
            except Exception as E:
                fails.append((player[1], str(E)))
                continue
        
        try:
            x, y = get_mmr_list(player[0])
        except Exception as E:
            fails.append((player[1], str(E)))
            continue

        plotted.append(player)
        x_values.append(x)
        y_values.append(y)

        if (rounddown(min(y)) < ymin):
            ymin = rounddown(min(y))
        
        if (roundup(max(y)) > ymax):
            ymax = roundup(max(y))

        if (len(y) > most_games):
            most_games = len(y)

    if len(plotted) == 0:
        return (False, fails, None)

    fig = Figure()
    ax = fig.subplots()
    ax.set_ylim([ymin,ymax])
    
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

    ax.set_yticks(y_ticks)
    ax.set_yticklabels([ranks.get(value, str(value)) for value in y_ticks])

    for i in range(len(plotted)):
        p = ax.plot(x_values[i], y_values[i], label=plotted[i][1])
        colour = p[0].get_color()
        ax.axhline(y=y_values[i][-1], color=colour, linestyle='--')

    ax.set_xlabel("Games played")
    ax.set_ylabel("MMR")
    ax.set_title("change in MMR over time")
    ax.legend()

    key = hashlib.sha1(','.join(sorted(player[0] for player in plotted)).encode()).hexdigest()[:12]
    filename = f"multigraph_{key}.png"
    fig.savefig(f"{config.get('RES')}/{filename}", bbox_inches="tight")

    if len(fails) == 0:
        return (True, "", filename)
    else:
        return (True, fails, filename)

def date_graph(puuid):
    playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerlist.load()
    ign = playerlist.get_ign_by_puuid(puuid)

    if not ign:
        raise MissingException

    dates, y = get_dated_mmr_list(puuid)

    fig = Figure(figsize=(10, 5))
    # adjust_text needs a canvas with a renderer
    FigureCanvasAgg(fig)
    ax = fig.subplots()

    y_min, y_max = rounddown(min(y)), roundup(max(y))
    y_ticks, y_labels = generate_y_ticks(y_min, y_max)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_ylim([y_min - 15, y_max + 15])

    p = ax.plot(dates, y, marker='.', markersize=3)
    colour = p[0].get_color()
    ax.axhline(y=y[-1], color=colour, linestyle=':', label='Current MMR')
    ax.axhline(y=max(y), color=colour, linestyle='--', label='Peak MMR')

    for year in range(dates[0].year + 1, dates[-1].year + 1):
        ax.axvline(datetime(year, 1, 1), color='grey', linestyle='dotted')

    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    # Label the first, last, lowest and peak games with their dates
    marked = sorted({0, len(y) - 1, y.index(min(y)), y.index(max(y))})
    texts = [ax.text(dates[i], y[i], dates[i].strftime('%d/%m/%y'), size=8,
                     bbox=dict(boxstyle="round, pad=0.2", fc="cyan")) for i in marked]
    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle='->'))

    ax.set(xlabel='Date', ylabel='MMR')
    ax.set_title(ign + '\'s MMR over time')
    ax.legend(loc='lower right')

    filename = f"{puuid}_dates.png"
    fig.savefig(f"{config.get('MMR_GRAPH')}/{filename}", bbox_inches="tight")

    return filename, dates[0], dates[-1]
