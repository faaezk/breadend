import valorant
from datetime import datetime
import playerlist

players = playerlist.players


def update_all_elo_history():
    
    update_count = 0
    
    for i in range(0, len(players)):
        update_count += valorant.update_elo_history(players[i][0], players[i][1])
        #print("completed " + str(i + 1) + "/" + str(len(players)))

    return str(update_count) + " updates"

updates = update_all_elo_history()
now = datetime.now()
print("completed on: " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S") + " with " + updates)