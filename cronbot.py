import requests
import json
import table

table.createTables()
ids = table.getUserIds() if len(table.getUserIds()) >0 else "0"

data = ids.split(",")
multiList = [data[x:x+5] for x in range(0, len(data), 5)]

for i in multiList:
    ids = ",".join(i)
    res = requests.get('https://www.pop1stats.com/api/player/'+ids+'')
    dict = str(res.text)
    dataobj = json.loads(dict)

    for x in dataobj:
        userId = x["id"]
        resGames = int(x["stats"][0]["stats"]["games"]) if x["stats"][0]["stats"]["games"] is not None else 0
        bdStatus = table.getStatus(userId) if table.getStatus(userId) is not None else "Offline"
        bdGames = table.getGames(userId) if table.getGames(userId) is not None else 0
        if bdStatus == "Offline":
            if resGames > 0 and bdGames < resGames:
                table.setStatus(userId, "Online")
                table.setGames(userId, resGames)
            if bdGames > resGames:
                table.setGames(userId, resGames)
        else:
            if bdGames == resGames or resGames == 0:
                table.setStatus(userId, "Offline")
                # print("ok")
            else:
                table.setGames(userId, resGames)

# print(table.getAllData())
