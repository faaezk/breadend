from playerlist import player

class Player():
    def __init__(self, ign, tag, name = None, onlineList = False, online = False):
        self.ign = ign
        self.tag = tag
        self.name = name
        self.onlineList = onlineList
        self.online = online
    
    def isOnline(self) -> bool:
        return self.isOnline
    
    def getCsv(self) -> str:
        return f"{self.ign},{self.tag},{self.name},{self.onlineList}\n"

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

    
    def getPlayers(self):
        return self.players
    
    def getOnlinePlayers(self):
        onlinePLayers = []
        for player in self.players:
            if player.onlineList:
                onlinePLayers.append(player)
        return onlinePLayers

if __name__ == "__main__":
    playerList = PlayerList("tempPlayerList.csv")
    playerList.add(Player("dilka30003", "0000", "dhiluka"))
    playerList.add(Player("dilka40004", "0000", "alsodhiluka"))
    playerList.add(Player("dilka50005", "0000", "againalsodhiluka"))
    playerList.add(Player("dilka60006", "0000", "woah!againalsodhiluka"))
    playerList.save()