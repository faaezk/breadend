import csv
class player:
    def __init__(self, player):
        self.ign = player[0]
        self.tag = player[1]
        self.name = player[2]
        if len(player) == 4:  self.online = player[3]
        else: self.online = False

def readCSV(path):
    out = []
    with open(path, newline="\n") as file:
        reader = csv.reader(file)
        for person in reader:
            out.append(player(person)) 
    return out

def writeCSV(file, list):
    with open(file, mode="w", newline="\n") as file:
        writer = csv.writer(file)
        [writer.writerow([person.ign, person.tag, person.name, person.online]) for person in list]

playerlist = readCSV("playerlist.csv")
writeCSV("playerlist.csv", playerlist)

players = [("silentwhispers", "0000"), 
    ("fakinator", "4269"), 
    ("faqinator", "7895"), 
    ("8888", "nadi"), 
    ("dilka30003", "0000"),
    ("slumonaire", "oce"),
    ("katchampion", "oce"), 
    ("imabandwagon", "oce"), 
    ("giroud", "8383"), 
    ("oshaoshawott", "oce"), 
    ("yovivels", "1830"), 
    ("therealrobdez", "3333"),
    ("bento2", "box"), 
    ("hoben222", "9327"), 
    ("jokii", "oce"),
    ("lyçhii", "mai"),
    ("lmao", "6548"),
    ("jack", "ytb"),
    ("vkj", "4084"),
    ("tallewok", "6209"),
    ("fade", "1280"),
    ("skzcross", "oce"),
    ("lol", "4529"),
    ("crossaxis", "mippl"),
    ("azatory", "nike"),
    ("quyteriyaki", "oce"), 
    ("talizorahrayya", "3303"), 
    ("quackinator", "2197")
    ]

online_players = [ 
    ["fakinator", "4269"],
    ["8888", "nadi"], 
    ["dilka30003", "0000"],
    ["slumonaire", "oce"],
    ["hoben222", "9327"],
    ["silentwhispers", "0000"],
    ["imabandwagon", "oce"],
    ["lmao", "6548"]
    ]

names = {"fakinator" : "Faaez", "8888" : "Hadi", "dilka30003" : "Dhiluka", 
        "slumonaire" : "Chris", "hoben222" : "Ben", "silentwhispers" : "Rasindu",
        "imabandwagon" : "Dylan", "lmao" : "Joseph"}

game_names = {"Faaez" : "fakinator", "Hadi" : "8888", "Dhiluka" : "dilka30003", 
        "Chris" : "slumonaire", "Ben" : "hoben222", "Rasindu" : "silentwhispers",
        "Dylan" : "imabandwagon", "Joseph" : "lmao"}

def get_attribute(value, attribute):

    if attribute == "ign":

        for player in playerlist:
            if player.name == value:
                return player.ign

    if attribute == "name":

        for player in playerlist:
            if player.ign == value:
                return player.name