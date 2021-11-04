import valorant
from datetime import datetime
import playerclass
#import graphs

def update_all_elo_history():
    
    playerList = playerclass.PlayerList('playerlist.csv')
    playerList.load()

    update_count = 0
    thing = ""
    
    for i in range(0, len(playerList.players)):

        thing = valorant.update_elo_history(playerList.players[i].ign, playerList.players[i].tag)

        if thing == "welp":
            return ["welp", i]

        update_count += int(thing)

        #print("completed " + str(i + 1) + "/" + str(len(playerList.players)))
        #graphs.make_graph(playerList.players[i].ign)

    return str(update_count) + " updates"

if __name__ == '__main__':
    updates = update_all_elo_history()
    now = datetime.now()
    
    if updates[0] == "welp":
        print("welp at " + str(updates[1]) + ": " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S"))

    else:
        print("completed on: " + now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S") + " with " + updates)