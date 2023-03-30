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

    for i, player in enumerate(playerList.players):
        if player.active == 'False':
            continue

        thing = valorant.update_database(player.puuid)

        if not thing[0]:

            retry.append(player)
            error_count += 1

            if printer:
                print(f'{i+1:02d}/{total}: {thing[1]} at {player.ign}')

        else:
            new_games = int(thing[1])
            update_count += new_games

            if new_games > 0:
                updatedList.append((player.ign, new_games))
                
            if graph:
                graphs.graph(puuid=player.puuid, ign=player.ign, update=False)
        
            if printer:
                print(f'{i+1:02d}/{total}: Success')

    total = len(retry)
    for i, player in enumerate(retry):
        thing = valorant.update_database(player.puuid)

        if not thing[0]:
            error_count += 1

            if printer:
                print(f'{i+1:02d}/{total}: {thing[1]} at {player.ign}')

        else:
            update_count += int(thing[1])

            if int(thing[1]) > 0:
                updatedList.append((player.ign, thing[1]))
                
            if graph:
                graphs.graph(puuid=player.puuid, ign=player.ign, update=False)
        
            if printer:
                print(f'{(i+1):02d}/{total}: Success on 2nd attempt')

    with open('ztemp.txt','w') as f:
        f.write(str(updatedList))

    if printer:
        print(updatedList)

    if error_count == 0:
        updates = f'{update_count} updates'
    else:
        updates = f'{update_count} updates, {error_count} errors'

    melb_now = datetime.now()
    
    printerz = f'completed on: {melb_now.strftime("%d/%m/%y")} at {melb_now.strftime("%H:%M:%S")} with {updates}'
    f = open("updater_log-2023.out", "a")
    f.write(printerz + '\n')
    f.close()

    return printerz

if __name__ == "__main__":
    update_all(False)