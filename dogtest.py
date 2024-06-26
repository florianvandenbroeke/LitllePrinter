from io import BytesIO
from PIL import Image, ImageOps
import requests, json

URL = 'https://dog.ceo/api/breeds/image/random'


def get_dog():
    im_url = json.loads(requests.get(URL).content)["message"]
    return im_url


print(get_dog())
