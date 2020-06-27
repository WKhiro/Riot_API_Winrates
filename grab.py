# Wesley Kok

import requests

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatchHistory(region, ID, APIKey, games):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + ID + "?endIndex=" + games + "&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatch(region, matchID, APIKey):
    URL = "https://" + region + ".api.riotgames.com/lol/match/v4/matches/" + matchID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestChampions():
    URL = "https://ddragon.leagueoflegends.com/cdn/10.13.1/data/en_US/champion.json"
    response = requests.get(URL)
    return response.json()

def serverInput():
    # All servers
    regionList = {"NA" : "na1",
                  "EUW" : "euw1",
                  "EUNE" : "eun1",
                  "BR" : "br1",
                  "LAN" : "la1",
                  "LAS" : "la2",
                  "OCE" : "oc1",
                  "KR" : "kr",
                  "TR" : "tr1",
                  "RU" : "ru",
                  "JP" : "jp1"}

    print("List of Servers: NA, EUW, EUNE, BR, LAN, LAS, OCE, KR, TR, RU, JP")
    inputRegion = (str)(input("Server: "))
    while inputRegion not in regionList:
        inputRegion = (str)(input("Invalid server, please choose from the given list of servers: "))
    return regionList[inputRegion]

def summonerNameInput(realRegion, APIKey):
    summonerName = (str)(input("Summoner Name: "))
    summonerJSON = requestSummonerData(realRegion, summonerName, APIKey)
    
    while "status" in summonerJSON:
        print(summonerName + " was not found.")
        summonerName = (str)(input("Summoner Name: "))
        summonerJSON = requestSummonerData(realRegion, summonerName, APIKey)
    return summonerName

def loadInChampions():
    allChamps = {}
    champJSON = requestChampions()["data"]
    for champ in champJSON:
        allChamps[champJSON[champ]["key"]] = champJSON[champ]["id"]
    return allChamps

def main():

    # Input secret Riot API key
    APIKey = (str)(input("API Key: "))

    realRegion = serverInput()
    summonerName = summonerNameInput(realRegion, APIKey)
    allChamps = loadInChampions()
    
    if (str)(input("Specific Champion? y/n ")) == "y":
        championDefault = (str)(input("Champion: "))
    else:
        championDefault = ""

    games = (int)(input("Games to query for (1 - 80): "))
    while games < 1 or games > 80:
        games = (str)(input("Invalid number of games, please choose from the given range (1 - 80): "))
    
    print("Analyzing...")

    allMatchIDs = []
    allResults = []
    remakes = 0

    # Get encrypted account ID
    summonerJSON = requestSummonerData(realRegion, summonerName, APIKey)
    accountID = (str)(summonerJSON["accountId"])

    # Get match history up to a limit
    historyJSON = requestMatchHistory(realRegion, accountID, APIKey, (str)(games))

    # Get the ID of each match in the queried match history
    for match in historyJSON["matches"]:
        allMatchIDs.append((str)(match["gameId"]))

    # Get the result and champion played in each match
    # Takes like 0.1 - 0.2 seconds per match
    for matchID in allMatchIDs:
        singleMatch = requestMatch(realRegion, matchID, APIKey)
        # Queue IDs for Ranked Solo/Duo, Normal, Ranked Flex in that order (450 if want ARAM) 900 for URF
        if singleMatch["queueId"] in {420, 430, 440, 450, 900}:
            if singleMatch["gameDuration"] < 300:
                remakes += 1
            else:
                # Get the summoner's participant ID to track down their stats
                for z in singleMatch["participantIdentities"]:
                    if z["player"]["accountId"] == accountID:
                        partId = (z["participantId"])
                        break

                # -1 since participants start at 1
                stats = singleMatch["participants"][partId - 1]["stats"]
                champion = (str)(singleMatch["participants"][partId - 1]["championId"])
                winLoss = (str)(stats["win"])
                kills = stats["kills"]
                deaths = stats["deaths"]
                assists = stats["assists"]
                row = [champion, winLoss, kills, deaths, assists]
                allResults.append(row)

    # Count up the data 
    counter = wins = tK = tD = tA =  0
    for x in allResults:
        if championDefault != "":
            if allChamps[x[0]] == championDefault:
                if x[1] == "True":
                    wins += 1
                counter += 1
                tK += x[2]
                tD += x[3]
                tA += x[4]
        else:
            if x[1] == "True":
                wins += 1
            counter += 1
            tK += x[2]
            tD += x[3]
            tA += x[4]

    # Account for champion selected or not
    if championDefault != "":
        if counter != 0:        
            print("Win rate in the last " + (str)(games) + " games with "
                  + (str)(championDefault) + " : " + (str)(round((wins/counter)*100, 2))
                  + "\n" + (str)(wins) + " wins out of " + (str)(counter)
                  + " games" + "\nRemakes: " + (str)(remakes))
        elif counter == 0:
            print(championDefault + " was not played by " + summonerName + " in the last " + games + " games")
    else:       
        print("Win rate in the last " + (str)(games) + " games: "
              + (str)(round((wins/counter)*100, 2)) + "\n" + (str)(wins) + " wins out of " + (str)(counter)
              + " games" + "\nRemakes: " + (str)(remakes))
    print("Total KDA:", tK, "/", tD, "/", tA)


if __name__ == "__main__":
    main()
