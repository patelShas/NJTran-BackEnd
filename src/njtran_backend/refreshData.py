from datetime import date
import json
import requests
from njtran_backend.paths import CONFIG_PATH, TOKENS_PATH


def getTokenFromNJTransit():
    with open(CONFIG_PATH) as f:
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
    if not TOKENS_PATH.exists():
        # data/ is gitignored, so it may not exist on a fresh clone
        TOKENS_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKENS_PATH.write_text("{}")
    with open(TOKENS_PATH, "r+") as f:
        tokens = json.load(f)
        today = str(date.today())
        if today not in tokens:
            token = getTokenFromNJTransit()
            tokens[today] = token
            f.seek(0)
            json.dump(tokens, f)
            f.truncate()
            
def getCurrentToken():
    with open(TOKENS_PATH, "r") as f:
        tokens = json.load(f)
        today = str(date.today())
        if today in tokens:
            return tokens[today]
        else:
            raise Exception("No token found for today's date. Please call updateToken() to get a new token.")

