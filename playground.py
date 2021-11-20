import playerclass

playerlist = playerclass.PlayerList("playerlist.csv")
playerlist.load()

print(playerlist.inList(playerclass.Player('fakinator', '4269')))