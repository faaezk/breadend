import requests
from datetime import datetime

import graphs
import config
import valorant
import playerclass

def update_all(graph=True, output=False, printer=True):

    playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerlist.load()
    playerlist.sort()

    update_count = 0
    dataless_count = 0
    errors_count = 0
    updates_list = []
    errors_list = []
    total = str(len(playerlist))

    puuid_list = playerlist.get_puuid_list()
    try:
        data_list = valorant.get_data("MMR_HISTORY_BY_PUUID", puuid_list=puuid_list)
    except Exception:
        pass

    for i, elem in enumerate(data_list):
        playerlist.get_player(elem[0])

        if 'name' in elem[1].keys() and elem[1]['name'] != None:
            update = valorant.update_database(puuid=elem[0], data=elem[1])
            new_games = int(update)
            update_count += new_games
            if new_games > 0:
                updates_list.append((elem[1]['name'], new_games))

            if graph:
                graphs.graph(puuid=elem[0], update=False)

            if printer:
                print(f'{i+1:02d}/{total}: Success')
        
        elif elem[1]['status'] == 200:
            ign = playerlist.get_ign_by_puuid(elem[0])
            print(f'{i+1:02d}/{total}: No games found for {ign}')
            dataless_count += 1
        else:
            ign = playerlist.get_ign_by_puuid(elem[0])
            errors_list.append(ign)
            print(f'{i+1:02d}/{total}: Error at {ign}')
            errors_count += 1

    if printer:
        print(updates_list)

    updates = f'{update_count} updates'
    if dataless_count > 0:
        updates += f', {dataless_count} dataless players'
    if errors_count > 0:
        updates += f', {errors_count} errors'

    curr_time = datetime.now()
    log_msg = f'completed on {curr_time.strftime("%d/%m/%y")} at {curr_time.strftime("%H:%M:%S")} with {updates}'

    if output:
        with open('ztemp.txt','w') as f:
            f.write(log_msg + '\n')
            f.write(str(updates_list))
    
    update_msg = ""
    for (player, updates) in updates_list:
        update_msg += f"{player}: {updates}, "
    update_msg = "**No Updates**" if update_msg == "" else f"**Updates:** {update_msg[:-2]}"

    errors_msg = ""
    for player in errors_list:
        errors_msg += f"{player}, "
    errors_msg = "**No Errors**" if errors_msg == "" else f"**Errors:** {errors_msg[:-2]}"

    with open(config.get("LOG_FP"), 'a') as f:
        f.write(log_msg + '\n')

    payload = {"username": "The Updater", "content": f'{log_msg}\n- {update_msg}\n- {errors_msg}'}
    requests.post(config.get("WEBHOOK_URL"), json=payload)
    return log_msg

if __name__ == "__main__":
    update_all()
