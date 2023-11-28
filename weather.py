import secret_stuff
import requests
import json

def get_weather(city_id, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric".format(city_id, api_key)
    r = requests.get(url)
    return r.text

def main():
    weather = get_weather(secret_stuff.get("CITY_ID"), secret_stuff.get("WEATHER_KEY"))
    john = json.loads(weather)

    return john