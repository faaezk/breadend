import valorant
from datetime import datetime
import playerclass
import graphs

def update_all(graph, printer=True,start=0):
    
    playerList = playerclass.PlayerList('playerlist.csv')
    playerList.load()
    playerList.sort()

    update_count = 0
    error_count = 0
    updatedList = []
    retry = []
    total = str(len(playerList.players) - start)

    for i in range(start, len(playerList.players)):
        player = playerList.players[i]

        if player.active == 'False':
            continue

        thing = valorant.update_database(player.puuid)

        if not thing[0]:

            if player.priority == '1':
                retry.append(player)
            
            error_count += 1

            if printer:
                print(f'{thing[1]} at {player.ign}')

        else:
            update_count += int(thing[1])

            if int(thing[1]) > 0:
                updatedList.append((player.ign, thing[1]))
                
            if graph:
                graphs.make_graph(puuid=player.puuid, ign=player.ign, update=False)
        
        if printer:
            print(f'completed {i+1}/{total}')
    
    i = 0
    total = len(retry)
    for player in retry:
        i += 1
        if player.active == 'False':
            continue

        thing = valorant.update_database(player.puuid)

        if not thing[0]:
            error_count += 1

            if printer:
                print(f'{thing[1]} at {player.ign}')

        else:
            error_count -= 1
            update_count += int(thing[1])

            if int(thing[1]) > 0:
                updatedList.append((player.ign, thing[1]))
                
            if graph:
                graphs.make_graph(puuid=player.puuid, ign=player.ign, update=False)
        
        if printer:
            print(f'completed retry {i+1}/{total}')


    if printer:
        print(updatedList)

    if error_count == 0:
        updates = f'{update_count} updates'
    else:
        updates = f'{update_count} updates, {error_count} errors'

    melb_now = datetime.now()
    
    printerz = f'completed on: {melb_now.strftime("%d/%m/%y")} at {melb_now.strftime("%H:%M:%S")} with {updates}'
    f = open("updater_log-2022.out", "a")
    f.write(printerz + '\n')
    f.close()

    return printerz

if __name__ == "__main__":
    update_all(False)