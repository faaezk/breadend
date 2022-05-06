import valorant
from datetime import datetime
#import pytz
import playerclass
import graphs

def update_all_elo_history(start=0):
    
    playerList = playerclass.PlayerList('playerlist.csv')
    playerList.load()

    update_count = 0
    thing = ""
    
    for i in range(start, len(playerList.players)):

        if playerList.players[i].active == 'False':
            continue

        thing = valorant.update_database(playerList.players[i].ign, playerList.players[i].tag)

        if thing == "welp":
            print("update count: " + str(update_count))
            return ["welp", i]
        if type(thing) != str:
            update_count += int(thing)

        print("completed " + str(i + 1) + "/" + str(len(playerList.players)))
        #graphs.make_graph(playerList.players[i].ign)

    return str(update_count) + " updates"

if __name__ == '__main__':
    updates = update_all_elo_history(0)
    #tz = pytz.timezone('Australia/Melbourne')
    melb_now = datetime.now()

    if updates[0] == "welp":
        printerz = "welp at " + str(updates[1]) + ": " + melb_now.strftime("%d/%m/%Y") + " at " + melb_now.strftime("%H:%M:%S")

    else:
        printerz = "completed on: " + melb_now.strftime("%d/%m/%Y") + " at " + melb_now.strftime("%H:%M:%S") + " with " + updates
    
    f = open("updater_log-2022.out", "a")
    f.write(printerz)
    f.close()

    print(printerz)