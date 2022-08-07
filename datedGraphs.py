from turtle import left
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

def mark_graph(texts, x, yint, ydates, i, marked, r):

    if i < 0:
        i = len(yint) - 1

    if i not in marked:
        texts.append(plt.text(s=ydates[i], x=x[i], y=yint[i], bbox=dict(boxstyle="round, pad=0.2", fc="cyan"), size=8.0))

        for j in range(i - r, i + r):
            if j >= 0 and j not in marked:
                if j == len(yint):
                    break
                marked.append(j)
        

    return marked, texts

def graph():
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
    for i in range(len(y)):
        yint.append(int(y[i].split(',')[0]))
        ts = y[i].split(',')[1].split('-')
        ydates.append(f'{ts[2]}/{months[ts[1]]}')
        
        added = False
        for year in years:
            if ts[3] == year[0]:
                added = True
                if x[i] > year[1]:
                    year[1] = x[i]
            
        if not added:
            years.append([ts[3], i])

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
    
    r = math.floor(len(yint)/7.0)
    marked = []
    topRightTexts = []
    botRightTexts = []
    topLeftTexts = []
    botLeftTexts = []

    peakMMRIndex = get_index(yint, max(yint))
    bottomMMRIndex = get_index(yint, min(yint))

    if peakMMRIndex != 0 and yint[peakMMRIndex] != yint[-1] and yint[peakMMRIndex - 1] > yint[peakMMRIndex + 1]:
        marked, topLeftTexts = mark_graph(topLeftTexts, x, yint, ydates, peakMMRIndex, marked, r)
    else:
        marked, topLeftTexts = mark_graph(topLeftTexts, x, yint, ydates, peakMMRIndex, marked, r)

    if bottomMMRIndex != 0 and yint[bottomMMRIndex] != yint[-1] and yint[bottomMMRIndex - 1] > yint[bottomMMRIndex + 1]:
        marked, botLeftTexts = mark_graph(botLeftTexts, x, yint, ydates, bottomMMRIndex, marked, r)
    else:
        marked, botRightTexts = mark_graph(botRightTexts, x, yint, ydates, bottomMMRIndex, marked, r)

    if yint[0] < yint[1]:
        marked, botRightTexts = mark_graph(botRightTexts, x, yint, ydates, 0, marked, r)
    else:
        marked, topRightTexts = mark_graph(topRightTexts, x, yint, ydates, 0, marked, r)

    if yint[-1] < yint[-2]:
        marked, botLeftTexts = mark_graph(botLeftTexts, x, yint, ydates, -1, marked, r)
    else:
        marked, topLeftTexts = mark_graph(topLeftTexts, x, yint, ydates, -1, marked, r)

    for i in range(len(yint)):
        if i not in marked:
            if yint[i - 2] < yint[i] and yint[i - 1] < yint[i]:
                marked, topLeftTexts = mark_graph(topLeftTexts, x, yint, ydates, i, marked, r)
            elif yint[i - 2] > yint[i] and yint[i - 1] > yint[i]:
                marked, botLeftTexts = mark_graph(botLeftTexts, x, yint, ydates, -1, marked, r)
            
            elif yint[i + 2] < yint[i] and yint[i + 1] < yint[i]:
                marked, topRightTexts = mark_graph(topRightTexts, x, yint, ydates, 0, marked, r)
            elif yint[i + 2] > yint[i] and yint[i + 1] > yint[i]:
                marked, botRightTexts = mark_graph(botRightTexts, x, yint, ydates, 0, marked, r)

    for year in years:
        plt.axvline(year[1], linestyle="dotted", color="k", label=year[0])

    adjust_text(topRightTexts, arrowprops=dict(arrowstyle='->'), force_points=(20, 30), force_text=(30, 30))
    adjust_text(botRightTexts, arrowprops=dict(arrowstyle='->'), force_points=(20, -40), force_text=(30, 30))

    adjust_text(botLeftTexts, arrowprops=dict(arrowstyle='->'), force_points=(-70, -40), force_text=(30, 30))
    adjust_text(topLeftTexts, arrowprops=dict(arrowstyle='->'), force_points=(-70, 30), force_text=(30, 30))

    colour = p[0].get_color()
    plt.axhline(yint[-1], linestyle="dashed", color=colour, label='Current MMR')
    plt.xlabel('Games played')
    plt.ylabel('MMR')
    plt.title('MMR over tifme')
    plt.legend(loc='upper left')
    plt.savefig('date-graph.png', bbox_inches="tight")


graph()
