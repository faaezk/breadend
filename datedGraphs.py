import matplotlib.pyplot as plt
import math
from adjustText import adjust_text

def minmax_in_range(y:list, index:int, john):
    if john == "max":
        bigjohn = max(y)

    if john == "min":
        bigjohn = min(y)

    for i in range(0, index + 3):
        if i > len(y):
            break

        if y[i] == bigjohn:
            return (True, i)
    return (False, 0)

def get_index(y:list, value:int):
    for i in range(0, len(y)):
        if y[i] == value:
            return i

ranks = {
0 : "Iron 1", 100 : "Iron 2", 200 : "Iron 3",
300 : "Bronze 1", 400 : "Bronze 2", 500 : "Bronze 3",
600 : "Silver 1", 700 : "Silver 2", 800 : "Silver 3",
900 : "Gold 1", 1000 : "Gold 2", 1100 : "Gold 3",
1200 : "Platinum 1", 1300 : "Platinum 2", 1400 : "Platinum 3",
1500 : "Diamond 1", 1600 : "Diamond 2", 1700 : "Diamond 3",
1800 : "Ascendant 1", 1900 : "Ascendant 2", 2000 : "Ascendant 3",
2100 : "Immortal 1", 2200 : "Immortal 2", 2300 : "Immortal 3"
}

months = {"January" : 1, "February" : 2, "March" : 3, 
          "April" : 4, "May" : 5, "June" : 6,
          "July" : 7, "August" : 8, "September" : 9, 
          "October" : 10, "November" : 11, "December" : 12}

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def rounddown(x):
    return int(math.floor(x / 100.0)) * 100

def markgraph(marked, x, yint, ydates, i):

    if i == 0:
        if yint[i] > yint[i+1]:
            plt.annotate(ydates[i], 
                        xy=(x[i], yint[i]), 
                        xytext=(x[i] - 4, yint[i] + 30),
                        arrowprops={'arrowstyle' : '->', 'shrinkA' : 1, 'shrinkB' : 4},
                        bbox=dict(boxstyle="round, pad=0.1", fc="yellow"))
        else:
            plt.annotate(ydates[i], 
                        xy=(x[i], yint[i]), 
                        xytext=(x[i] - 4, yint[i] - 30),
                        arrowprops={'arrowstyle' : '->', 'shrinkA' : 1, 'shrinkB' : 4},
                        bbox=dict(boxstyle="round, pad=0.1", fc="yellow"))


    elif yint[i] > yint[i-1]:
        plt.annotate(ydates[i], 
                    xy=(x[i], yint[i]), 
                    xytext=(x[i] - 4, yint[i] + 30),
                    arrowprops={'arrowstyle' : '->', 'shrinkA' : 1, 'shrinkB' : 4},
                    bbox=dict(boxstyle="round, pad=0.1", fc="yellow"))


    else:
        plt.annotate(ydates[i], 
                    xy=(x[i], yint[i]), 
                    xytext=(x[i] - 4, yint[i] - 30),
                    arrowprops={'arrowstyle' : '->', 'shrinkA' : 1, 'shrinkB' : 4},
                    bbox=dict(boxstyle="round, pad=0.1", fc="yellow"))


    marked.append(i)
    return marked

def agraph():
    y = ["1724,Sunday-July-10-2022-7:42-AM", "1707,Sunday-July-10-2022-8:18-AM", "1700,Sunday-July-10-2022-9:14-AM", "1721,Sunday-July-10-2022-9:52-AM", 
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
        "1800,Wednesday-July-20-2022-8:19-AM"]

    x = list(range(1, len(y) + 1))
    total = len(y)
    num = 0

    if num > 1 and (num - 1) < len(y):
        y = y[-num:]
    else:
        num = 0
        total = 0

    yint = []
    ydates = []
    for i in range(0, len(y)):
        yint.append(int(y[i].split(',')[0]))
        ts = y[i].split(',')[1].split('-')
        ydates.append(f'{ts[2]}/{months[ts[1]]}/{str(ts[3][2:])}')

    ymin = rounddown(min(yint) - 1) + 50
    ymax = roundup(max(yint) + 1) + 25

    axes = plt.gca()
    axes.set_ylim([ymin,ymax])

    ticks = []
    i = int(math.floor((ymin) / 50.0)) * 50

    ranger = int((ymax-ymin)/100)

    while i <= int(math.ceil(ymax / 25.0)) * 25:
        ticks.append(i)
        if ranger == 1:
            i += 20
        elif ranger < 4:
            i += 25
        elif ranger < 8:
            i += 50
        else:
            i += 100

    axes.set_yticks(ticks)
    labely = []

    for value in ticks:
        if value % 100 != 0:
            labely.append(str(value))

        else:
            labely.append(ranks[value])

    tickx = []  
    i = 0
    j = 0

    if len(x) <= 15:
        j = 1
    elif len(x) < 30:
        j = 2
    elif len(x) < 70:
        j = 5
    elif len(x) < 150:
        j = 10

    if len(x) < 150:
        while i <= len(x):
            tickx.append((total - num) + i)
            i += j

        if x[-1] not in tickx:
            if (x[-1] - tickx[-1]) < 4:
                tickx[-1] = x[-1]
            else:
                tickx.append(x[-1])

        axes.set_xticks(tickx)

    axes.set_yticklabels(labely)
    p = plt.plot(x, yint, 'bx-')
    marked = []

    peakMMRIndex = get_index(yint, max(yint))
    bottomMMRIndex = get_index(yint, min(yint))
    marked = markgraph(marked, x, yint, ydates, peakMMRIndex)
    marked = markgraph(marked, x, yint, ydates, bottomMMRIndex)
    marked = markgraph(marked, x, yint, ydates, 0)
    marked = markgraph(marked, x, yint, ydates, -1)

    i = 0
    while i < len(yint):
        mark = True
        for j in range((i - 3), (i + 3)):
            if j in marked:
                mark = False
                break
            
        if mark:
            marked = markgraph(marked, x, yint, ydates, i)
        
        i += 10


    colour = p[0].get_color()
    plt.axhline(y=y[-1], color=colour, linestyle='dotted')
    plt.xlabel('Games played')
    plt.ylabel('MMR')
    plt.title('MMR over tie')
    plt.savefig('date-graph.png', bbox_inches="tight")

def mark_grapha(texts, x, yint, ydates, i):
    texts.append(plt.text(s=ydates[i], x=x[i], y=yint[i], bbox=dict(boxstyle="round, pad=0.2", fc="cyan"), size=8.0))
    return texts

def cgraph():
    y = ["1724,Sunday-July-10-2022-7:42-AM", "1707,Sunday-July-10-2022-8:18-AM", "1700,Sunday-July-10-2022-9:14-AM", "1721,Sunday-July-10-2022-9:52-AM", 
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
        "1800,Wednesday-July-20-2022-8:19-AM"]

    x = list(range(1, len(y) + 1))
    total = len(y)
    num = 0

    if num > 1 and (num - 1) < len(y):
        y = y[-num:]
    else:
        num = 0
        total = 0

    yint = []
    ydates = []
    years = []
    for i in range(0, len(y)):
        yint.append(int(y[i].split(',')[0]))
        ts = y[i].split(',')[1].split('-')
        ydates.append(f'{ts[2]}/{months[ts[1]]}')
        
        added = False
        for year in years:
            if ts[3][2:] == year[0]:
                added = True
                if i > year[1]:
                    year[1] = i
            
        if not added:
            years.append([ts[3][2:], i])

    ymin = rounddown(min(yint) - 1) + 50
    ymax = roundup(max(yint) + 1) + 25

    axes = plt.gca()
    axes.set_ylim([ymin,ymax])

    ticks = []
    i = int(math.floor((ymin) / 50.0)) * 50

    ranger = int((ymax-ymin)/100)

    while i <= int(math.ceil(ymax / 25.0)) * 25:
        ticks.append(i)
        if ranger == 1:
            i += 20
        elif ranger < 4:
            i += 25
        elif ranger < 8:
            i += 50
        else:
            i += 100

    axes.set_yticks(ticks)
    labely = []

    for value in ticks:
        if value % 100 != 0:
            labely.append(str(value))

        else:
            labely.append(ranks[value])

    tickx = []  
    i = 0
    j = 0

    if len(x) <= 15:
        j = 1
    elif len(x) < 30:
        j = 2
    elif len(x) < 70:
        j = 5
    elif len(x) < 150:
        j = 10

    if len(x) < 150:
        while i <= len(x):
            tickx.append((total - num) + i)
            i += j

        if x[-1] not in tickx:
            if (x[-1] - tickx[-1]) < 4:
                tickx[-1] = x[-1]
            else:
                tickx.append(x[-1])

        axes.set_xticks(tickx)

    axes.set_yticklabels(labely)
    p = plt.plot(x, yint, 'b-')
    
    marked = []
    texts = []

    peakMMRIndex = get_index(yint, max(yint))
    bottomMMRIndex = get_index(yint, min(yint))
    texts = mark_grapha(texts, x, yint, ydates, peakMMRIndex)
    texts = mark_grapha(texts, x, yint, ydates, bottomMMRIndex)
    texts = mark_grapha(texts, x, yint, ydates, 0)
    texts = mark_grapha(texts, x, yint, ydates, -1)
    
    marked.append(peakMMRIndex)
    marked.append(bottomMMRIndex)
    marked.append(0)
    marked.append(-1)

    i = 5
    while i < len(ydates):
        mark = True
        for j in range((i - 5), (i + 5)):
            if j in marked:
                mark = False
                break
            
        if mark:
            texts = mark_grapha(texts, x, yint, ydates, i)
            marked.append(i)
        
        i += 10

    for year in years:
        plt.vlines(year[1], ymin, ymax, linestyles ="dotted", colors ="k", label=f'20{year[0]}')

    adjust_text(texts, arrowprops=dict(arrowstyle='->'), force_points=30)

    colour = p[0].get_color()
    plt.axhline(y=y[-1], color=colour, linestyle='dotted')
    plt.xlabel('Games played')
    plt.ylabel('MMR')
    plt.title('MMR over time')
    plt.legend(loc='upper left')
    plt.savefig('date-graph.png', bbox_inches="tight")


cgraph()
