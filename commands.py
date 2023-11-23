import sys
import valorant
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


if func == 'leaderboard':
    region = sys.argv[2]
    update = sys.argv[3]
    output = leaderboard(region, update)

print(str(output))
sys.stdout.flush()

