from PIL import Image
import requests
from io import BytesIO

url = "https://dog.ceo/api/breeds/image/random"

print(requests.get(url))