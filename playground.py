from datetime import datetime
import pytz

now = datetime.now()

tz = pytz.timezone('Australia/Melbourne')
melb_now = datetime.now(tz)



#print(now.strftime("%d/%m/%Y") + " at " + now.strftime("%H:%M:%S"))
#print(melb_now.strftime("%d/%m/%Y") + " at " + melb_now.strftime("%H:%M:%S"))

import valorant
import elo_history_updater

elo_history_updater.update_all_elo_history()
valorant.elo_leaderboard()
john = ""
f = open("leaderboard.txt", "r")
for x in f:
    john += x
f.close()
