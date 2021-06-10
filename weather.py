import configparser
import requests
from pprint import pprint
import json

def get_config():
    c = configparser.ConfigParser()
    c.read('/home/ubuntu/DBot/config.ini')

    return c['openweathermap']['api'], c['openweathermap']['city_id'], c['discord']['token']


def get_weather(city_id, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric".format(city_id, api_key)
    r = requests.get(url)
    return r.text


def main():
    config = get_config()
    api_key = config[0]
    city_id = config[1]
    weather = get_weather(city_id, api_key)

    john = json.loads(weather)

    return john


print(main())
