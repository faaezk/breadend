import valorant
from datetime import datetime
import playerclass

def update_all_elo_history():
    
    playerList = playerclass.PlayerList('playerlist.csv')
    playerList.load()

    update_count = 0
    
    for i in range(0, len(playerList.players)):
        update_count += valorant.update_elo_history(playerList.players[i].ign, playerList.players[i].tag)
        #print("completed " + str(i + 1) + "/" + str(len(playerList.players)))

    return str(update_count) + " updates"

if __name__ == "__main__":
    print("johnjohn")