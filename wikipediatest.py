import datetime as dt
import requests
import json
from random import randint

def get_picture():

    today = dt.datetime.now()
    date = today.strftime("%Y/%m/%d")

    URL = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/" + "2024/06/23"
    response = json.loads(requests.get(URL).text)

    im_URL = response["image"]["thumbnail"]["source"]
    im_desc = response["image"]["description"]["text"]

    return im_URL, im_desc


def get_history():

    today = dt.datetime.now()
    date = today.strftime("%m/%d")
    URL = 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/' + date
    response = json.loads(requests.get(URL).text)
    eventlist = response["selected"]
    event = randint(0, len(eventlist) - 1)

    title = eventlist[event]["text"]
    year = eventlist[event]["year"]

    return title, year

print(get_history())