from playerlist import player
import requests
import json

class Player():
    def __init__(self, ign, tag, name = None, onlineList = False, online = False, status = None, partyid = False, partysize = 0):
        self.ign = ign
        self.tag = tag
        self.name = name
        self.onlineList = onlineList
        self.online = online

        self.status = status
        self.partyid = partyid
        self.partysize = partysize

    def isOnline(self) -> bool:
        return self.isOnline
    
    def getCsv(self) -> str:
        return f"{self.ign},{self.tag},{self.name},{self.onlineList}\n"

    def __str__(self) -> str:
        return f"{self.ign}#{self.tag}"

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)

    def updatestuff(self):
        url = "https://api.henrikdev.xyz/valorant/v1/live-match/{}/{}".format(self.ign, self.tag)
        r = requests.get(url, headers={'Cache-Control': 'no-cache'})
        data = json.loads(r.text)

        igstatus = ""

        if data['status'] == '200':
            
            self.partyid = data['data']['party_id']

            if data['data']['current_state'] == 'MENUS':
                self.partysize = data['data']['party_size']

            state = data['data']['current_state']

            if state == 'PREGAME':
                igstatus = "Online and in agent select"

            elif state == 'MENUS':
                igstatus = "Online and in menu"

            elif state == 'INGAME':
                map = data['data']['map']

                if map == 'Range':
                    igstatus = "Online in the range"

                else:
                    game_mode = data['data']['gamemode']
                    score = str(data['data']['score_ally_team']) + '-' + str(data['data']['score_enemy_team'])
                    map = data['data']['map']
                    igstatus = "Online in " + game_mode + " going " + score + " on " + map
        else:
            igstatus = "Offline"
        
        self.status = igstatus



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