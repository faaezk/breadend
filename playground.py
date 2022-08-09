
import beta_playerclass
import os

playerList = beta_playerclass.PlayerList('playerlistb.csv')
playerList.load()

folder = 'mmr_history'
fileList = []

for player in playerList.players:
    fileList.append(f'{player.ign}.txt')

for file in os.listdir(folder):

    if file in fileList:
        old_name = os.path.join(folder, file)
        ign = os.path.splitext(file)[0]

        puuid = playerList.get_puuid_by_ign(ign)
        new_base = f"{puuid}.txt"
        new_name = os.path.join(folder, new_base)
        os.rename(old_name, new_name)

res = os.listdir(folder)
print(res)
