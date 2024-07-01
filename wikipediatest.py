import datetime as dt
import requests
import json
from PIL import Image, ImageOps
from io import BytesIO
from random import randint

def get_picture():

    today = dt.datetime.now()
    date = today.strftime("%Y/%m/%d")

    URL = "https://api.wikimedia.org/feed/v1/wikipedia/en/featured/" + date
    response = json.loads(requests.get(URL, timeout=10).text)

    im_URL = response["image"]["thumbnail"]["source"]
    im_desc = response["image"]["description"]["text"]

    im_data = requests.get(im_URL, timeout=10).content
    stream = BytesIO(im_data)
    im = ImageOps.grayscale(Image.open(stream))

    return im, im_desc


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
