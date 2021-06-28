import temp

playerList = []
onlinerz = []

def loadData():

    global playerList
    global onlinerz
    playerList = temp.PlayerList("playerlist.csv")
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

        temp = []

        while current_party == inparty[i][1]:
            temp.append(inparty[j][0])
            j += 1
            if j == len(inparty):
                break
            current_party = inparty[j][1]

        parties.append(temp)
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

        temp = ""
        for player in parties[i]:
            temp = temp + player + ", "

        temp = temp[:-2]

        if randos == 1:
            temp += " (with " + str(randos) + " other person)"
        if randos > 1:
            temp += " (with " + str(randos) + " other people)"

        final.append((("Party " + str(i + 1)), temp))

    return final

if __name__ == "__main__":
    loadData()
    print(main())