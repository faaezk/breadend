import config
import valorant
import playerclass

playerlist = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
playerlist.load()

data_list = valorant.get_data("ACCOUNT_BY_PUUID", puuid_list=playerlist.get_puuid_list())
for player in playerlist:
    data = None
    for elem in data_list:
        if player.puuid == elem[0]:
            player.ign = elem[1]['data']['name'].lower()
            player.tag = elem[1]['data']['tag'].lower()
            break

playerlist.save()