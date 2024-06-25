from io import BytesIO
from PIL import Image, ImageOps
import requests, json

URL = 'https://dog.ceo/api/breeds/image/random'

def get_dog():
    return ImageOps.grayscale(Image.open(BytesIO(requests.get(json.loads(requests.get(URL).content)["message"]).content)))
