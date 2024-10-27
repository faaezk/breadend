import json
import requests
from datetime import datetime

import graphs
import config
import valorant
import playerclass
from times import update_file_entries

def update_all(graph=True, output=False, printer=True):

    playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerlist.load()
    playerlist.sort()

    update_count = 0
    dataless_count = 0
    errors_count = 0
    updates_list = []
    errors_lists = {}
    total = str(len(playerlist))

    puuid_list = playerlist.get_puuid_list()
    data_list = valorant.get_data("MMR_HISTORY_BY_PUUID", puuid_list=puuid_list)

    for i, (puuid, data) in enumerate(data_list):
        if 'name' in data.keys() and data['name'] != None:
            update = valorant.update_database(puuid=puuid, data=data)
            new_games = int(update)
            update_count += new_games
            if new_games > 0:
                updates_list.append((data['name'], new_games))

            if printer:
                print(f'{i+1:02d}/{total}: Success')
        
        elif 'status' in data.keys() and data['status'] == 200:
            ign = playerlist.get_ign_by_puuid(puuid)
            print(f'{i+1:02d}/{total}: No games found for {ign}')
            dataless_count += 1
        else:
            ign = playerlist.get_ign_by_puuid(puuid)
            if data['error'] in errors_lists.keys():
                errors_lists[data['error']].append(ign)
            else:
                errors_lists[data['error']] = [ign]
            
            print(f'{i+1:02d}/{total}: Error at {ign}')
            errors_count += 1

    if graph:
        for player in playerlist:
            graphs.graph(puuid=player.puuid, update=False)

    if printer:
        print(updates_list)

    updates = f'{update_count} updates'
    if dataless_count > 0:
        updates += f', {dataless_count} dataless players'

    try:
        # Get errors from file
        with open(config.get("MMR_ERRORS_LIST"), 'r') as f:
            prev_errors = json.load(f)

        # Overwrite new errors into file
        with open(config.get("MMR_ERRORS_LIST"), 'w') as f:
            json.dump(errors_lists, f)

        # Remove repeated errors for log message
        for error in prev_errors:
            if error in errors_lists.keys():
                for player in prev_errors[error]:
                    errors_lists[error].remove(player)
                if len(errors_lists[error]) == 0:
                    del errors_lists[error]
    except:
        pass

    if errors_count > 0:
        updates += f', {errors_count} errors'

    curr_time = datetime.now()
    log_msg = f'completed on {curr_time.strftime("%d/%m/%y")} at {curr_time.strftime("%H:%M:%S")} with {updates}'

    if output:
        with open('ztemp.txt','w') as f:
            f.write(log_msg + '\n')
            f.write(str(updates_list))
    
    update_msg = ""
    for (ign, updates) in updates_list:
        update_msg += f"{ign}: {updates}, "
    update_msg = "**No Updates**" if update_msg == "" else f"**Updates:** {update_msg[:-2]}"

    errors_msg = ""
    for error in errors_lists.keys():
        msg = ""
        for ign in errors_lists[error]:
            msg += f'{ign}, '
        errors_msg += f'- {error}: {msg[:-2]}\n'
    errors_msg = "**No New Errors**" if errors_msg == "" else f"**Errors:**\n\t{errors_msg}"

    with open(config.get("LOG_FP"), 'a') as f:
        f.write(log_msg + '\n')

    payload = {"username": "The Updater", "content": f'{log_msg}\n- {update_msg}\n- {errors_msg}'}
    requests.post(config.get("WEBHOOK_URL"), json=payload)
    return log_msg

if __name__ == "__main__":
    try:
        update_file_entries()
    except:
        pass

    try:
        update_all()
    except:
        pass
