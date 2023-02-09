import sys
sys.path.append('../')

from flask import Flask, request
import json
import requests
from funcs import location

app = Flask(__name__)


def get_weather(latitude, longitude):
    loc = location.get_location(latitude, longitude)
    api_key = "0f08ae3944df4253b5a145322230902"
    city_name = loc[-4]
    days = 250

    forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_name}&days={days}"

    response = requests.get(forecast_url)

    if response.status_code == 200:
        forecast_data = response.json()
        print(forecast_data)
    else:
        print("Failed to get weather forecast")
    

@app.route('/', methods=['GET'])
def main():
    return

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    get_weather('22.4797693', '88.294758')