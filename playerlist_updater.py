import requests
from datetime import datetime

import config
import valorant
import playerclass

playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
playerlist.load()

data_list = valorant.get_data("ACCOUNT_BY_PUUID", puuid_list=playerlist.get_puuid_list())
changes = []

for player in playerlist:
    data = None
    for elem in data_list:
        if player.puuid == elem[0] and 'data' in elem[1].keys():
            ign = elem[1]['data']['name'].lower()
            tag = elem[1]['data']['tag'].lower()
            if (player.ign != ign) or (player.tag != tag):
                changes.append((f"{player.ign}#{player.tag}", f"{ign}#{tag}"))
                player.ign = ign
                player.tag = tag
            break

curr_time = datetime.now()
msg = f'completed on {curr_time.strftime("%d/%m/%y")} at {curr_time.strftime("%H:%M:%S")}\n'

playerlist.save()
if len(changes) == 0:
    msg += "**No Username Changes**"
else:
    msg += "**Username Changes:**\n"
    for (old, new) in changes:
        msg += f"- {old} -> {new}\n"
    msg = msg[:-1]

payload = {"username": "The Updater", "content": msg}
requests.post(config.get("WEBHOOK_URL"), json=payload)