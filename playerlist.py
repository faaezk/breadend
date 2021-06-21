import csv

global_path = "playerlist.csv"

class player:
    def __init__(self, player):
        self.ign = player[0]
        self.tag = player[1]
        self.name = player[2]
        if len(player) == 4: 
            self.online = (player[3] == "True")
        else: 
            self.online = False

    def __str__(self):
        return f'{self.ign}, {self.tag}, {self.name}, {self.online}'

def readCSV(path):
    out = []
    with open(path, newline="\n") as file:
        reader = csv.reader(file)
        for person in reader:
            out.append(player(person)) 
    return out

def writeCSV(file, data):
    with open(file, mode="w", newline="\n") as file:
        writer = csv.writer(file)
        [writer.writerow([person.ign, person.tag, person.name, person.online]) for person in data]

players = readCSV(global_path)
writeCSV(global_path, players)

online_players = [i for i in players if i.online == True]

def get_player(key, value):
    if (key == "name" or key == "ign") == False: 
        raise KeyError(f'We don\'t take {key} here.')

    for player in players:
        if vars(player)[key] == value: 
            return player

    raise KeyError(f'We can\'t find a {key} for {value}')

get_player("name", "Faaez")