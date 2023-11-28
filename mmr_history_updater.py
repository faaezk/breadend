import valorant
from datetime import datetime
import playerclass
import graphs
import secret_stuff
import requests

def update_all(graph=True, output=False, printer=True,start=0):
    
    playerlist = playerclass.PlayerList(secret_stuff.get("PLAYERLIST_FP"))
    playerlist.load()
    playerlist.sort()

    thing = None
    update_count = 0
    error_count = 0
    updatedList = []
    retry = []
    total = str(len(playerlist) - start)

    for i, player in enumerate(playerlist):
        if player.active == 'False':
            continue
        
        try:
            thing = valorant.update_database(player.puuid)
        except Exception as E:
            retry.append(player)
            error_count += 1
            if printer:
                print(f'{i+1:02d}/{total}: {E.message} at {player.ign}')
            continue

        new_games = int(thing)
        update_count += new_games

        if new_games > 0:
            updatedList.append((player.ign, new_games))
            
        if graph:
            graphs.graph(puuid=player.puuid, update=False)
    
        if printer:
            print(f'{i+1:02d}/{total}: Success')

    total = len(retry)
    for i, player in enumerate(retry):

        try:
            thing = valorant.update_database(player.puuid)
        except Exception as E:
            error_count += 1
            if printer:
                print(f'{i+1:02d}/{total}: {E.message} at {player.ign}')

        thing = int(thing)
        update_count += thing

        if thing > 0:
            updatedList.append((player.ign, thing))
            
            if graph:
                graphs.graph(puuid=player.puuid, update=False)
    
        if printer:
            print(f'{(i+1):02d}/{total}: Success on 2nd attempt')

    if printer:
        print(updatedList)

    if error_count == 0:
        updates = f'{update_count} updates'
    else:
        updates = f'{update_count} updates, {error_count} errors'

    melb_now = datetime.now()
    
    printerz = f'completed on: {melb_now.strftime("%d/%m/%y")} at {melb_now.strftime("%H:%M:%S")} with {updates}'
    
    if output:
        with open('ztemp.txt','w') as f:
            f.write(printerz + '\n')
            f.write(str(updatedList))

    with open(secret_stuff.get("LOG_FP"), 'a') as f:
        f.write(printerz + '\n')

    embed = {
        "title": f'{melb_now.strftime("%d/%m/%y")} at {melb_now.strftime("%H:%M:%S")}',
        "description": f'{updates}: {updatedList}'
    }

    payload = {
        "content": "",
        "username": "The Updater",
        "embeds": [embed]
    }

    requests.post(secret_stuff.get("WEBHOOK_URL"), json=payload)

    return printerz

if __name__ == "__main__":
    update_all()