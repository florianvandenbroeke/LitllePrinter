import datetime as dt
import requests
import json

def get_picture():

    today = dt.datetime.now()
    date = today.strftime("%Y/%m/%d")

    URL = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/" + date
    response = json.loads(requests.get(URL).text)

    print(response["image"]["thumbnail"]["source"])

get_picture()