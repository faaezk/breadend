import playerclass

playerList = playerclass.PlayerList('playerlist.csv')
playerList.load()
playerList.change_ign('workgffding', 'actuallyworking', 'yay')
playerList.save()