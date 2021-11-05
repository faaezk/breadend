import valorant
from datetime import datetime
import pytz
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
    tz = pytz.timezone('Australia/Melbourne')
    melb_now = datetime.now(tz)

    if updates[0] == "welp":
        print("welp at " + str(updates[1]) + ": " + melb_now.strftime("%d/%m/%Y") + " at " + melb_now.strftime("%H:%M:%S"))

    else:
        print("completed on: " + melb_now.strftime("%d/%m/%Y") + " at " + melb_now.strftime("%H:%M:%S") + " with " + updates)