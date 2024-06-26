class Player():
    def __init__(self, ign, tag, puuid, priority = 2, active = True):
        self.ign = ign
        self.tag = tag
        self.puuid = puuid
        self.priority = priority
        self.active = active
    
    def getCsv(self) -> str:
        return f"{self.ign},{self.tag},{self.puuid},{self.priority},{self.active}\n"

    def __str__(self) -> str:
        return f"{self.ign}#{self.tag},{self.puuid}"

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)
    
    def setUser(self, ign, tag):
        self.ign = ign
        self.tag = tag
    
    def setPriority(self, priority):
        self.priority = priority

class PlayerList():
    def __init__(self, filePath):
        self.filePath = filePath
        self.players = []

    def __iter__(self):
        return iter(self.players)
    
    def __next__(self):
        return next(self.players)
    
    def __len__(self):
        return len(self.players)
    
    def add(self, player: Player):
        self.players.append(player)

    def remove(self, ign):
        tag = self.get_tag_by_ign(ign)
        puuid = self.get_puuid_by_ign(ign)
        player = Player(ign.lower(), tag, puuid)

        if not self.inList(player):
            return "Player not in list"
        else:
            self.players.remove(player)
            return f'{ign}#{tag} has been removed'

    def save(self):
        with open(self.filePath, "w+") as f:
            f.writelines([x.getCsv() for x in self.players])

    def load(self):
        with open(self.filePath, 'r') as f:
            for line in f:
                playerData = line.split(',')
                ign = playerData[0]
                tag = playerData[1]
                puuid = playerData[2]
                priority = playerData[3]
                active = playerData[4][:-1]
                self.players.append(Player(ign, tag, puuid, priority, active))
    
    def sort(self):
        self.players.sort(key=lambda x: x.priority)
    
    def getPlayers(self):
        return self.players
    
    def get_player(self, puuid):
        for player in self.players:
            if player.puuid == puuid:
                return player
        
        return False

    def get_puuid_list(self, active):
        puuid_list = []
        for player in self.players:
            if active:
                if player.active:
                    puuid_list.append(player.puuid)
            else:
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
            if elem.ign == old_ign:
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
            if elem.ign == ign:
                player = elem
                break

        if player == None:
            return False

        player.setPriority(priority)        
        self.save()

        return True

    def get_puuid_by_ign(self, ign):
        for player in self.players:
            if ign == player.ign:
                return player.puuid
        return False
    
    def get_ign_by_puuid(self, puuid):
        for player in self.players:
            if puuid == player.puuid:
                return player.ign
        return ''
    
    def get_tag_by_ign(self, ign):
        for player in self.players:
            if ign == player.ign:
                return player.tag
        return False