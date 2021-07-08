import playerclass
import json
import requests

playerList = []
onlinerz = []

def loadData():

    global playerList
    global onlinerz
    playerList = playerclass.PlayerList("playerlist.csv")
    playerList.load()
    onlinerz = playerList.getOnlinePlayers()

    return

def getPlayer(name):
    for onliner in onlinerz:
        if onliner.name == name:
            return onliner
    
    return

def form_parties():

    global onlinerz
    inparty = []

    for player in onlinerz:

        if player.partyid == False:
            continue

        inparty.append([player.name, player.partyid])
    
    inparty.sort(key=lambda x: str(x[-1]))

    if inparty == []:
        return []
    
    current_party = inparty[0][1]
    parties = []
    i = 0
    j = 0

    while i < len(inparty):

        playerclass = []

        while current_party == inparty[i][1]:
            playerclass.append(inparty[j][0])
            j += 1
            if j == len(inparty):
                break
            current_party = inparty[j][1]

        parties.append(playerclass)
        i = j

    return parties


def main():

    parties = form_parties()
    final = [("Players Online", "")]

    for player in onlinerz:

        if player.status:
            final.append((player.name.ljust(8), player.status))

    if len(final) == 1:
        final = [("All players offline", "")]
        return final
    
    final.append(("Parties:", ""))

    for i in range(0, len(parties)):

        randos = 0
        leader = getPlayer(parties[i][0])
        party_size = len(parties[i])
        
        if leader.partysize > 0:
            randos = leader.partysize - party_size

        playerclass = ""
        for player in parties[i]:
            playerclass = playerclass + player + ", "

        playerclass = playerclass[:-2]

        if randos == 1:
            playerclass += " (with " + str(randos) + " other person)"
        if randos > 1:
            playerclass += " (with " + str(randos) + " other people)"

        final.append((("Party " + str(i + 1)), playerclass))

    return final

def addPlayer(msg):
    playerList = playerclass.PlayerList("playerlist.csv")
    playerList.load()
    inpot = msg.split(' ')
    user = inpot[1].split('#')

    if len(user) != 2:
        return False
        
    ignn, tagg = user

    if len(inpot) == 3:
        namee = inpot[2]
    else:
        namee = ignn

    url = "https://api.henrikdev.xyz/valorant/v1/mmr-history/ap/{}/{}".format(ignn, tagg)
    r = requests.get(url)

    if str(r) == "<Response [204]>":
        return False

    john = json.loads(r.text)

    if john['status'] == '404' or john['status'] == '500':
        return False
    
    if inpot[0] == "$addonline" or inpot[0] == "=addonline":
        if playerList.inList(playerclass.Player(ignn, tagg)):
            playerList.remove(playerclass.Player(ignn, tagg))
        
        playerList.add(playerclass.Player(ignn, tagg, namee, True))
    
    else:
        if playerList.inList(playerclass.Player(ignn, tagg)):
            return True
        
        playerList.add(playerclass.Player(ignn, tagg, namee))
        
    playerList.save()

def removePlayer(msg):
    playerList = playerclass.PlayerList("playerlist.csv")
    playerList.load()
    inpot = msg.split(' ')
    user = inpot[1].split('#')

    if len(user) != 2:
        return False

    ignn, tagg = user

    if len(inpot) == 3:
        namee = inpot[2]
    else:
        namee = ignn

    if playerList.inList(playerclass.Player(ignn, tagg)) == False:
        return False

    if inpot[0] == "$removeonline" or inpot[0] == "=removeonline":
        playerList.remove(playerclass.Player(ignn, tagg, namee))
        playerList.add(playerclass.Player(ignn, tagg, namee))

    else:
        playerList.remove(playerclass.Player(ignn, tagg, namee))
    
    playerList.save()



if __name__ == "__main__":
    # faq = "$removeonline quackinator#2197"

    # print(removePlayer(faq))

    # playerlist = playerclass.PlayerList('playerlist.csv')
    # playerlist.load()

    # x = playerlist.getOnlinePlayers()
    # for player in x:
    #     print(player.name)

    loadData()
    print(main())