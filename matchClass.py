import requests
import json
import datetime

weapons = {
"2f59173c-4bed-b6c3-2191-dea9b58be9c7" : "knife",
"29a0cfab-485b-f5d5-779a-b59f85e204a8" : "classic",
"42da8ccc-40d5-affc-beec-15aa47b42eda" : "shorty",
"1baa85b4-4c70-1284-64bb-6481dfc3bb4e" : "ghost",
"e336c6b8-418d-9340-d77f-7a9e4cfe0702" : "sheriff",
"c4883e50-4494-202c-3ec3-6b8a9284f00b" : "marshall",
"462080d1-4035-2937-7c09-27aa2a5c27a7" : "spectre",
"ec845bf4-4f79-ddda-a3da-0db3774b2794" : "judge",
"910be174-449b-c412-ab22-d0873436b21b" : "bucky",
"ae3de142-4d85-2547-dd26-4e90bed35cf7" : "bulldog",
"a03b24d3-4319-996d-0f8c-94bbfba1dfc7" : "operator",
"63e6c2b6-4a8e-869c-3d4c-e38355226584" : "odin",
"55d8a0f4-4274-ca67-fe2c-06ab45efdf58" : "ares",
"9c82e19d-4575-0200-1a81-3eacf00cf872" : "vandal",
"ee8e8d15-496b-07ac-e5f6-8fae5d4c7b1a" : "phantom",
"4ade7faa-4cf1-8376-95ef-39884480959b" : "guardian",
"44d4e95c-4157-0037-81b2-17841bf2e8e3" : "frenzy",
"f7e1b454-4ad4-1063-ec0a-159e56b58941" : "stinger",
"Ultimate" : "Ultimate", "Ability1" : "Ability 1",
"Ability2" : "Ability 2", "Ability3" : "Ability 3", "Ability4" : "Ability 4"
}

class Player():
    def __init__(self, ign, tag, team, character, rank, stats, ability_use, damage_done, damage_taken):
        self.ign = ign.lower()
        self.tag = tag.lower()
        self.team = team.lower()
        self.agent = character
        self.rank = rank
        self.kda = stats
        self.ability_use = ability_use
        self.damage_done = damage_done
        self.damage_taken = damage_taken
    
    def getName(self):
        return f'{self.ign}#{self.tag}'
    
    def getKDA(self) -> str:
        return "{}/{}/{}".format(self.kda['kills'], self.kda['deaths'], self.kda['assists'])
    
    def getScore(self) -> int:
        return self.kda['score']



class Event():
    def __init__(self, time, killer, deather, weapon_id, killer_location, deather_location):
        self.time = time
        self.killer = killer
        self.deather = deather
        self.weapon_id = weapon_id
        self.killer_location = killer_location
        self.deather_location = deather_location

    def getWeapon(self):
        global weapons
        return weapons[self.weapon_id]


class Round():
    def __init__(self, winner, ending, plant, defuse):
        self.winner = winner
        self.ending = ending
        self.plant = plant
        self.defuse = defuse
        self.events = []
        self.nextRound = None
        self.lastRound = None

    def addEvents(self, events: list):
        for player in events:
            for event in player['kill_events']:

                killer = event['killer_display_name']
                killer_location = None
                for person in event['player_locations_on_kill']:
                    if person['player_display_name'] == killer:
                        killer_location = person['location']
                        break

                temp = Event(event['kill_time_in_round'], killer, 
                            event['victim_display_name'], event['damage_weapon_id'],
                            killer_location, event['victim_death_location'])
                
                self.events.append(temp)

    def addEvent(self, event: Event):       
        self.events.append(event)

    def set_nextRound(self, round):
        self.nextRound = round

    def set_lastRound(self, round):
        self.lastRound = round


class Match():
    def __init__(self, map, mode, matchid, time):
        self.map = map
        self.mode = mode
        self.matchid = matchid
        self.time = datetime.datetime.fromtimestamp(time/1000.0 + 36000).strftime('%H:%M %p %d/%m/%y')
        self.redTeam = []
        self.blueTeam = []
        self.rounds = []
        self.score = []
        self.winner = ""

    def addPlayers(self, players:list, team):
        for player in players:
            temp = Player(player['name'], player['tag'], player['team'],
                player['character'], player['currenttier_patched'], 
                player['stats'], player['ability_casts'], player['damage_made'], player['damage_received'])
            if team == 'blue':
                self.blueTeam.append(temp)
            if team == 'red':
                self.redTeam.append(temp)

    def addRound(self, round:Round):
        self.rounds.append(round)

    def addPlayer(self, player:Player, team):
        if team == 'blue':
            self.blueTeam.append(player)
        if team == 'red':
            self.redTeam.append(player)

    def setScore(self, name:str, teams:dict):
        team = ""
        for player in self.redTeam:
            if player.getName() == name.lower():
                team = player.team()
                break
        if team == "":
            team = "blue"
        
        self.score = [teams[team]['rounds_won'], teams[team]['rounds_lost']]
        
        if teams[team]['has_won'] == True:
            self.winner = team
        else:
            if team == 'blue':
                self.winner = 'red'
            else:
                self.winner = 'blue'

    def getScore(self):
        return f'{self.score[0]} - {self.score[1]}'

    def getRedTeamStats(self):
        stats = []
        rounds = self.score[0] + self.score[1]
        
        self.redTeam.sort(key=lambda x: x.getScore(), reverse=True)
        for player in self.redTeam:
            acs = player.getScore()/rounds
            stats.append([player.getName(), player.agent, acs, player.getKDA()])
        
        return stats
        
    def getBlueTeamStats(self):
        stats = []
        rounds = self.score[0] + self.score[1]
        
        self.blueTeam.sort(key=lambda x: x.getScore(), reverse=True)
        for player in self.blueTeam:
            acs = player.getScore()/rounds
            stats.append([player.getName(), player.agent, acs, player.getKDA()])
        
        return stats

def get_data(ign, tag, game):
    
    if game not in ['1','2','3','4','5']:
        return "invalid game index"

    url = "https://api.henrikdev.xyz/valorant/v3/matches/ap/{}/{}".format(ign, tag)
    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return False

    john = json.loads(r.text)

    if john['status'] == '404' or john['status'] == '500':
        return False
    
    return john['data'][int(game) - 1]

if __name__ == '__main__':

    data = get_data('quackinator', '2197', '1')
    if data != False:
        match = Match(data['metadata']['map'], data['metadata']['mode'], 
                    data['metadata']['matchid'], data['metadata']['game_start'])

        match.addPlayers(data['players']['red'], 'red')
        match.addPlayers(data['players']['blue'], 'blue')

        for round in data['rounds']:
            tempRound = Round(round['winning_team'], round['end_type'], 
                        round['bomb_planted'], round['bomb_defused'])

            tempRound.addEvents(round['player_stats'])
            match.addRound(tempRound)
