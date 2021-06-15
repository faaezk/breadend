import elo_history
from datetime import datetime

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


def update_all_elo_history():
    update_count = 0
    for i in range(0, len(players)):
        update_count += elo_history.update_elo_history(players[i][0], players[i][1])
        #print("completed " + str(i + 1) + "/" + str(len(players)))

    return str(update_count) + " updates"

updates = update_all_elo_history()
now = datetime.now()
print("completed on: " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S") + " with " + updates)