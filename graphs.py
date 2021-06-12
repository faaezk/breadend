import matplotlib.pyplot as plt
import os

players = [("silentwhispers", "0000"), 
    ("Fakinator", "4269"), 
    ("faqinator", "7895"), 
    ("8888", "nadi"), 
    ("dilka30003", "0000"),
    ("slumonaire", "oce"),
    ("KATCHAMPION", "oce"), 
    ("imabandwagon", "oce"), 
    ("giroud", "8383"), 
    ("oshaoshawott", "oce"), 
    ("YoVivels", "1830"), 
    ("therealrobdez", "3333"),
    ("bento2", "box"), 
    ("hoben222", "9327"), 
    ("jokii", "oce"),
    ("Lyçhii", "mai"),
    ("lmao", "6548"),
    ("jack", "ytb"),
    ("VKj", "4084"),
    ("TallEwok", "6209"),
    ("Fade", "1280"),
    ("SkzCross", "OCE"),
    ("lol", "4529"),
    ("Crossaxis", "mippl"),
    ("Azatory", "nike")
    ]

def make_graph(username):

    if os.path.isfile('elo_history/{}.txt'.format(username)) == False:
        return
    file1 = open('elo_history/{}.txt'.format(username), 'r')

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

    plt.savefig('elo_graphs/{}.png'.format(username))
    file1.close()
    plt.clf()

def make_all_graphs():
    for i in range(0, len(players)):
        make_graph(players[i][0])

make_all_graphs()