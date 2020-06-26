import requests

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + "na1" + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    #print(response.json())
    return response.json()

def requestRanked(region, ID, APIKey):
    URL = "https://" + "na1" + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatchHistory(region, ID, APIKey):
    URL = "https://" + "na1" + ".api.riotgames.com/lol/match/v4/matchlists/by-account/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestMatch(region, matchID, APIKey):
    URL = "https://" + "na1" + ".api.riotgames.com/lol/match/v4/matches/" + matchID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()
    
def main():
    region = ""
    summonerName = (str)(input("Name: "))
    APIKey = (str)(input("APIKey: "))
    #APIKey = (str)(input("API: "))
    responseJSON = requestSummonerData(region, summonerName, APIKey)

    ID = responseJSON["id"]
    accountID = responseJSON["accountId"]
    print("accountID: " + accountID)
    ID = str(ID)
    responseJSON2 = requestRanked(region, ID, APIKey)
    responseJSONH = requestMatchHistory(region, accountID, APIKey)
    #print(responseJSON2)
    #print(responseJSON2[0]["tier"])
    #responseTest = responseJSONH["matches"]
    #print([x["gameId"] for x in responseTest])
    responseMatch = (str)(responseJSONH["matches"][0]["gameId"])
    responseJSONSingle = requestMatch(region, responseMatch, APIKey)
    for x in responseJSONSingle["participantIdentities"]:
        if x["player"]["accountId"] == accountID:
            print("FOUND YA")
            print(x["player"]["accountId"])
    #print(responseJSONSingle["participantIdentities"][0]["player"]["accountId"])

if __name__ == "__main__":
    main()
