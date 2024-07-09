import playerclass, config
from datetime import datetime
import json
from graphs import multigraph

def graph(ign_list):
    playerList = playerclass.PlayerList(config.get("PLAYERLIST_FP"))
    playerList.load()
    ign_list = ign_list.split(',')
    puuid_list = []

    for ign in ign_list:
        puuid = playerList.get_puuid_by_ign(ign.split('#')[0].lower().strip())
        if puuid:
            puuid_list.append(puuid)

    if len(puuid_list) == 0:
        return False
    
    elif len(puuid_list) == 1:
        puuid = puuid_list[0]
        with open(f'{config.get("HISTORY_FP")}/{puuid}.txt') as f:
            for line in f:
                pass
            last_game = line.strip()
        
        content = ""

        # If last game is dated, extract day, month and year
        if len(last_game.split(',')) > 1:
            output_format = "%H:%M on %d/%m/%y"
            input_format = "%A-%B-%d-%Y-%I:%M-%p"
            
            date = datetime.strptime(last_game.split(',')[1], input_format)
            content = f'Last game recorded at {date.strftime(output_format)}'
        
        response = json.dumps({
            "content" : content, 
            "filepath" : f'{config.get("GRAPHS_FP")}/{puuid}.png'
        })

    else:
        res = multigraph(puuid_list)
        if res[0] == True:
            response = json.dumps({
                "content" : f"{res[1]}", 
                "filepath" : f'{config.get("MULTI_GRAPH_FP")}'
            })

        else:
            return False

    return response


print(graph("fakinator,dilka3003"))