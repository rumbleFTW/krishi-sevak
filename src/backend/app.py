import sys
sys.path.append('../')

from flask import Flask, request
import json
import requests
import pickle
import numpy as np
from funcs import location

app = Flask(__name__)

def get_soil(latitude, longitude):
    soils = {
        "Andhra Pradesh": ['red', 'alluvial', ],
        "Arunachal Pradesh": ['red', 'mountain', ],
        "Assam": ['laterite', 'alluvial', 'mountain', ],
        "Bihar": ['alluvial', ],
        "Chhattisgarh": ['red', ],
        "Goa": ['alluvial', 'laterite', ],
        "Gujarat": ['alluvial', 'black'],
        "Haryana": ['alluvial', ],
        "Himachal Pradesh": ['mountain', ],
        "Jharkhand": ['alluvial', ],
        "Karnataka": ['red', 'laterite', ],
        "Kerala": ['laterite', ],
        "Madhya Pradesh": ['laterite', ],
        "Maharashtra": ['black'],
        "Manipur": ['red', 'laterite', ],
        "Meghalaya": ['laterite', 'red', ],
        "Mizoram": ['red', ],
        "Nagaland": ['red', ],
        "Odisha": ['laterite', 'red'],
        "Punjab": ['alluvial', ],
        "Rajasthan": ['desert', ],
        "Sikkim": ['mountain', ],
        "Tamil Nadu": ['red', 'laterite', ],
        "Telangana": ['red', 'black'],
        "Tripura": ['red', ],
        "Uttar Pradesh": ['alluvial', ],
        "Uttarakhand": ['mountain', ],
        "West Bengal": ['alluvial', ]
    }
    pH = {
        'Andhra Pradesh': 6.4,
        'Arunachal Pradesh': 5.5,
        'Assam': 5.8,
        'Bihar': 6.5,
        'Chhattisgarh': 6.2,
        'Goa': 6.5,
        'Gujarat': 7.0,
        'Haryana': 8.0,
        'Himachal Pradesh': 6.0,
        'Jharkhand': 6.2,
        'Karnataka': 6.5,
        'Kerala': 6.2,
        'Madhya Pradesh': 6.8,
        'Maharashtra': 6.5,
        'Manipur': 5.8,
        'Meghalaya': 6.5,
        'Mizoram': 6.0,
        'Nagaland': 6.2,
        'Odisha': 6.5,
        'Punjab': 7.0,
        'Rajasthan': 8.5,
        'Sikkim': 5.8,
        'Tamil Nadu': 6.5,
        'Telangana': 6.2,
        'Tripura': 6.5,
        'Uttar Pradesh': 7.0,
        'Uttarakhand': 6.5,
        'West Bengal': 6.2
    }

    locname = locname = location.get_location(latitude, longitude)
    # return locname
    return soils[locname[-3].strip()], pH[locname[-3].strip()]

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
    model = pickle.load(open('../machine-learning/model', 'rb'))
    return json.dumps({
                        "result": ''.join(model.predict([
                            [   6.6,
                                23,
                                77,
                                57,
                                7,
                                0,
                                1,
                                0,
                                0,
                                0,
                                1,
                                0
                            ]
                            ])),
                        "loc": get_soil(22.478848, 88.2900992)
                        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)