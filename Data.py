from io import BytesIO
import json
import requests
from PIL import Image, ImageOps
import datetime as dt
from random import randint
from bs4 import BeautifulSoup

to = 5
API_ninja_key = "Fpg1VeRz4ELzZ1F+obZHXQ==7jDp8PXkGiEPzxk9"


def get_dog():

    URL = 'https://dog.ceo/api/breeds/image/random'

    try:
        # Get image URL of random dog
        im_url = json.loads(requests.get(URL, timeout=to).content)["message"]

        # Get image from URL
        im_data = requests.get(im_url, timeout=to).content
        stream = BytesIO(im_data)
        im = ImageOps.grayscale(Image.open(stream))
        return im

    except requests.exceptions.RequestException:
        return None


def get_quote():

    URL = 'https://api.api-ninjas.com/v1/quotes?category=inspirational'

    try:
        response = requests.get(URL, timeout=to, headers={'X-Api-key': API_ninja_key})

        if response.status_code == requests.codes.ok:
            response = json.loads(response.text)[0]
            return response["quote"], response["author"]
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def get_fact():

    URL = 'https://api.api-ninjas.com/v1/facts'

    try:
        response = requests.get(URL, timeout=to, headers={'X-Api-key': API_ninja_key})

        if response.status_code == requests.codes.ok:
            response = json.loads(response.text)[0]
            return response["fact"]
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def get_joke():

    URL = 'https://api.api-ninjas.com/v1/jokes'

    try:
        response = requests.get(URL, headers={'X-Api-key': API_ninja_key})

        if response.status_code == requests.codes.ok:
            response = json.loads(response.text)[0]
            return response["joke"]
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def get_history():

    try:
        today = dt.datetime.now()
        date = today.strftime("%m/%d")
        URL = 'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/' + date
        response = json.loads(requests.get(URL, timeout=to).text)
        eventlist = response["selected"]
        event = randint(0, len(eventlist) - 1)
        title = eventlist[event]["text"]
        year = eventlist[event]["year"]
        return title, year

    except requests.exceptions.RequestException:
        return None


def get_picture():

    try:
        today = dt.datetime.now()
        date = today.strftime("%Y/%m/%d")
        URL = "https://api.wikimedia.org/feed/v1/wikipeia/en/featured/" + date

        response = json.loads(requests.get(URL, timeout=to).text)
        im_URL = response["image"]["thumbnail"]["source"]
        im_desc = response["image"]["description"]["text"]

        im_data = requests.get(im_URL, timeout=to).content
        stream = BytesIO(im_data)
        im = ImageOps.grayscale(Image.open(stream))
        return im, im_desc

    except requests.exceptions.RequestException:
        return None
    except KeyError:
        return None


def get_news():

    soup = BeautifulSoup(requests.get("https://www.vrt.be/vrtnieuws/nl.rss.articles.xml").content, "xml")
    entries = soup.find_all("entry")
    titles = [entry.title.text for entry in entries]
    return titles


def get_date():
    now = dt.datetime.now()
    weekday = now.strftime("%A")
    day = str(now.day)
    month = now.strftime("%B")
    hour = str(now.hour)
    minute = str(now.minute)

    return weekday, day, month, hour, minute


print(get_date())
