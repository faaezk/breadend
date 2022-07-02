import valorant
from datetime import datetime
#import pytz
import playerclass
import graphs

def update_all_elo_history(start=0):
    
    playerList = playerclass.PlayerList('playerlistb.csv')
    playerList.load()
    playerList.sort()

    update_count = 0
    updatedList = []
    total = str(len(playerList.players) - start)

    for i in range(start, len(playerList.players)):
        player = playerList.players[i]

        if player.active == 'False':
            continue

        thing = valorant.update_database(player.ign, player.tag)

        if thing == "welp":
            print("update count: " + str(update_count))
            return ["welp", i]

        if type(thing) != str:
            update_count += int(thing)

            if int(thing) > 0:
                updatedList.append((player.ign, thing))
                
        #graphs.make_graph(player.ign, update=False)
        print("completed " + str(i + 1) + "/" + total)

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
    f.write(printerz + '\n')
    f.close()

    print(printerz)