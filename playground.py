import playerclass


playerlist = playerclass.PlayerList("playerlistb.csv")
playerlist.load()

playerlist.players.sort(key=lambda x: x.priority)

for player in playerlist.players:
    print(player.ign)

playerlist.save()