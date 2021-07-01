import valorant
from datetime import datetime
import temp

def update_all_elo_history():
    
    playerList = temp.PlayerList('playerlist.csv')
    playerList.load()

    update_count = 0
    
    for i in range(0, len(playerList.players)):
        update_count += valorant.update_elo_history(playerList.players[i].ign, playerList.players[i].tag)
        #print("completed " + str(i + 1) + "/" + str(len(playerList.players)))

    return str(update_count) + " updates"

updates = update_all_elo_history()
now = datetime.now()
print("completed on: " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S") + " with " + updates)