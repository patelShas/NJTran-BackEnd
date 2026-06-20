from datetime import date
import json
import requests



def getTokenFromNJTransit():
    with open("config.json") as f:
        config = json.load(f)

    url = "https://testraildata.njtransit.com/api/GTFSRT/getToken"
    headers = {"accept": "text/plain"}
    files = {
        "username": (None, config["username"]),
        "password": (None, config["password"]),
    }

    response = requests.post(url, headers=headers, files=files)
    return json.loads(response.text)["UserToken"]

def updateToken():
    # check "GTFS-tokens.json" to see if a token exists for today's date
    # if it does not, call getToken() to get a new token and save it in "GTFS-tokens.json" with today's date
    with open("GTFS-tokens.json", "r+") as f:
        tokens = json.load(f)
        today = str(date.today())
        if today not in tokens:
            token = getTokenFromNJTransit()
            tokens[today] = token
            f.seek(0)
            json.dump(tokens, f)
            f.truncate()
            
def getCurrentToken():
    with open("GTFS-tokens.json", "r") as f:
        tokens = json.load(f)
        today = str(date.today())
        if today in tokens:
            return tokens[today]
        else:
            raise Exception("No token found for today's date. Please call updateToken() to get a new token.")
