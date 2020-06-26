import requests

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + "na1" + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatchHistory(region, ID, APIKey):
    # End index 10 as a limit
    URL = "https://" + "na1" + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + ID + "?endIndex=10" + "&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatch(region, matchID, APIKey):
    URL = "https://" + "na1" + ".api.riotgames.com/lol/match/v4/matches/" + matchID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestChampions():
    URL = "https://ddragon.leagueoflegends.com/cdn/10.13.1/data/en_US/champion.json"
    response = requests.get(URL)
    return response.json()
    
def main():

    # Default na1
    region = ""
    summonerName = (str)(input("Name: "))

    # Input secret API key
    APIKey = ""

    allMatchIDs = []
    allResults = []

    # Get encrypted account ID
    summonerJSON = requestSummonerData(region, summonerName, APIKey)
    accountID = (str)(summonerJSON["accountId"])

    # Get match history up to a limit
    historyJSON = requestMatchHistory(region, accountID, APIKey)

    # Get the ID of each match in the queried match history
    for match in historyJSON["matches"]:
        allMatchIDs.append((str)(match["gameId"]))

    # Get the result and champion played in each match
    for matchID in allMatchIDs:
        singleMatch = requestMatch(region, matchID, APIKey)
        
        # Queue IDs for Ranked Solo/Duo, Normal, Ranked Flex in that order
        if singleMatch["queueId"] in {420, 430, 440}:
            # Get the summoner's participant ID to track down their stats
            for z in singleMatch["participantIdentities"]:
                if z["player"]["accountId"] == accountID:
                    partId = (z["participantId"])
            for y in singleMatch["participants"]:
                if y["participantId"] == partId:
                    winLoss = (str)(y["stats"]["win"])
                    champion = (str)(y["championId"])
                    row = [champion, winLoss]
                    allResults.append(row)
                    
    # Results and champion KEYS of each match
    print("Keyed Results:", allResults)

    # Switch them out for champion names
    champJSON = requestChampions()["data"]
    allChamps =[]
    for x in allResults:
        for y in champJSON:
            if x[0] == champJSON[y]["key"]:
                x[0] = champJSON[y]["id"]
    print(allResults)
    

if __name__ == "__main__":
    main()
