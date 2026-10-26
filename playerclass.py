class Player():
    def __init__(self, ign, tag, puuid, priority = 2):
        self.ign = ign
        self.tag = tag
        self.puuid = puuid
        self.priority = priority
    
    def getCsv(self) -> str:
        return f"{self.ign},{self.tag},{self.puuid},{self.priority}\n"

    def __str__(self) -> str:
        return f"{self.ign}#{self.tag},{self.puuid}"

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)
    
    def setUser(self, ign, tag):
        self.ign = ign
        self.tag = tag
    
    def setPriority(self, priority):
        self.priority = int(priority)

class PlayerList():
    def __init__(self, filePath):
        self.filePath = filePath
        self.players = []

    def __iter__(self):
        return iter(self.players)

    def __len__(self):
        return len(self.players)
    
    def add(self, player: Player):
        self.players.append(player)

    def remove(self, ign):
        ign = ign.lower()
        tag = self.get_tag_by_ign(ign)
        puuid = self.get_puuid_by_ign(ign)
        player = Player(ign, tag, puuid)

        if not self.inList(player):
            return "Player not in list"
        else:
            self.players.remove(player)
            self.save()
            return f'{ign}#{tag} has been removed'

    def save(self):
        with open(self.filePath, "w+") as f:
            f.writelines([x.getCsv() for x in self.players])

    def load(self):
        self.players = []
        with open(self.filePath, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                playerData = line.split(',')
                ign = playerData[0]
                tag = playerData[1]
                puuid = playerData[2]
                priority = int(playerData[3].strip())
                self.players.append(Player(ign, tag, puuid, priority))
    
    def sort(self):
        self.players.sort(key=lambda x: x.priority)
    
    def getPlayers(self):
        return self.players
    
    def get_player(self, puuid):
        for player in self.players:
            if player.puuid == puuid:
                return player
        
        return False

    def get_puuid_list(self):
        puuid_list = []
        for player in self.players:
            puuid_list.append(player.puuid)

        return puuid_list

    def inList(self, player: Player):
        for x in self.players:
            if x == player:
                return True
        
        return False

    def change_ign(self, old_ign, new_ign, tag):

        player = None
        for elem in self.players:
            if elem.ign.lower() == old_ign.lower():
                player = elem
                break

        if player == None:
            return False

        player.setUser(new_ign, tag)        
        self.save()

        return True

    def change_priority(self, ign, priority):

        player = None
        for elem in self.players:
            if elem.ign.lower() == ign.lower():
                player = elem
                break

        if player == None:
            return False

        player.setPriority(priority)        
        self.save()

        return True

    def get_puuid_by_ign(self, ign):
        for player in self.players:
            if ign.lower() == player.ign.lower():
                return player.puuid
        return False
    
    def get_ign_by_puuid(self, puuid):
        for player in self.players:
            if puuid == player.puuid:
                return player.ign
        return False
    
    def get_tag_by_ign(self, ign):
        for player in self.players:
            if ign.lower() == player.ign.lower():
                return player.tag
        return False