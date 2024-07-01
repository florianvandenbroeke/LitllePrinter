from io import BytesIO
from PIL import Image, ImageOps
import requests, json

URL = 'https://dog.ceo/api/breeds/image/random'


def get_dog():
    im_url = json.loads(requests.get(URL).content)["message"]
    im_data = requests.get(im_url).content
    stream = BytesIO(im_data)
    im = ImageOps.grayscale(Image.open(stream))
    return im

