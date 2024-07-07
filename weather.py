import json
import config
import requests

def get_weather(city_id, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric".format(city_id, api_key)
    r = requests.get(url)
    return r.text

def main():
    weather = get_weather(config.get("CITY_ID"), config.get("WEATHER_KEY"))
    john = json.loads(weather)

    return john