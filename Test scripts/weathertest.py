import datetime as dt
import requests

CITY = "Waregem"
API = "050a0f8de21a6a07e8008d8af2d7291d"


geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={CITY}&appid={API}"

coordinates = requests.get(geo_url).json()[0]
LAT = coordinates["lat"]
LON = coordinates["lon"]

forecast_url = f"https://api.openweathermap.org/data/2.5/forecast/?lat={LAT}&lon={LON}&appid={API}&units=metric&lang=nl&cnt=4"

forecast = requests.get(forecast_url).json()


for el in forecast["list"]:
    print(dt.datetime.fromtimestamp(el["dt"]))
    print(el)