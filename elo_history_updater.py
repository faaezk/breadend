import valorant
from datetime import datetime
import playerclass
import graphs

def update_all_elo_history(graph, start=0):
    
    playerList = playerclass.PlayerList('playerlist.csv')
    playerList.load()
    playerList.sort()

    update_count = 0
    error_count = 0
    updatedList = []
    total = str(len(playerList.players) - start)

    for i in range(start, len(playerList.players)):
        player = playerList.players[i]

        if player.active == 'False':
            continue

        thing = valorant.update_database(player.ign, player.tag)

        if not thing[0]:
            error_count += 1
            print(f'{thing[1]} at {player.ign}')

        else:
            update_count += int(thing[1])

            if int(thing[1]) > 0:
                updatedList.append((player.ign, thing[1]))
                
            if graph:
                graphs.make_graph(player.ign, update=False)
        
        print("completed " + str(i + 1) + "/" + total)

    print(updatedList)

    if error_count == 0:
        return f'{update_count} updates'
    else:
        return f'{update_count} updates, {error_count} errors'

def main(graph, start=0):
    updates = update_all_elo_history(graph, start)
    melb_now = datetime.now()

    printerz = f'completed on: {melb_now.strftime("%d/%m/%y")} at {melb_now.strftime("%H:%M:%S")} with {updates}'
    f = open("updater_log-2022.out", "a")
    f.write(printerz + '\n')
    f.close()

    return printerz

if __name__ == "__main__":
    print(main(False))