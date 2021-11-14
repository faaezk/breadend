class Player():
    def __init__(self, ign, tag, name = None, active = True):
        self.ign = ign
        self.tag = tag
        
        if name == None:
            self.name = ign
        else:
            self.name = name

        self.active = active
    
    def getCsv(self) -> str:
        return f"{self.ign},{self.tag},{self.name},{self.active}\n"

    def __str__(self) -> str:
        return f"{self.ign}#{self.tag}"

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)

class PlayerList():
    def __init__(self, filePath):
        self.filePath = filePath
        self.players = []
    
    def add(self, player:Player):
        self.players.append(player)
    
    def remove(self, player:Player):
        self.players.remove(player)

    def save(self):
        with open(self.filePath, "w+") as f:
            f.writelines([x.getCsv() for x in self.players])

    def load(self):
        with open(self.filePath, 'r') as f:
            for line in f.readlines():
                playerData = line.split(',')
                ign = playerData[0]
                tag = playerData[1]
                name = playerData[2]
                active = playerData[3][:-1]
                self.players.append(Player(ign, tag, name, active))
    
    def getPlayers(self):
        return self.players

    def inList(self, player:Player):
        for i in self.players:
            if i == player:
                return True
        
        return False

if __name__ == '__main__':
    playerList = PlayerList('playerlist.csv')
    playerList.load()
    print('yes')