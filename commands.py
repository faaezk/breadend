import sys
import json
import valorant
import playerclass
import secret_stuff
import mmr_history_updater

func = sys.argv[1]

def leaderboard(region, update):
    the_message = ""
    if region == 'local':
        if update == 'true':
            mmr_history_updater.update_all(False, printer=False)

        with open(secret_stuff.LOG_PATH,'r') as f:
            for lastLine in f:
                pass

        the_message = f"Last updated at {lastLine.split(' ')[4]}, {lastLine.split(' ')[2]}\n"

    the_message += valorant.leaderboard(region)
    return the_message

def stats(ign, tag):

    playerList = playerclass.PlayerList(secret_stuff.PLAYERLIST_PATH)
    playerList.load()
    puuid = playerList.get_puuid_by_ign(ign)

    if puuid == "None" and tag != 'emptytag':
        player_data = valorant.get_data("ACCOUNT_BY_NAME", ign=ign, tag=tag)
        puuid = player_data['data']['puuid']
    
    try:
        data = valorant.stats(puuid)
    except Exception as E:
        return json.dumps({"error" : E.message})

    tag = playerList.get_tag_by_ign(ign)
    
    if not data[0]:
        return json.dumps({"error" : "Player not found"})
    
    else:
        stats = data[0]
        fields = []

        for act in stats:
            fields.append({
                "name": act[0],
                "value": act[1]}
            )

        embed = {
            "title": "Competitive Statistics",
            "url": "https://youtu.be/kJa2kwoZ2a4?si=K_NtlL62gv2RwhDP",
            "author": f"{ign}#{tag}",
            "thumbnail": data[1],
            "fields": fields
        }

    return json.dumps(embed)


if func == 'leaderboard':
    region = sys.argv[2]
    update = sys.argv[3]
    output = leaderboard(region, update)

if func == 'stats':
    ign = sys.argv[2]
    tag = sys.argv[3]
    output = stats(ign, tag)

print(str(output))
sys.stdout.flush()
