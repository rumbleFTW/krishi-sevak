import sys
sys.path.append('../')

from flask import Flask, request
from funcs import location
import json
from funcs import location

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_soil():
    latitude = str(request.args.get('latitude'))
    longitude = str(request.args.get('longitude'))
    locname = location.get_location(latitude, longitude)

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

    # composition = {
    #     "alluvial": {"N": 0, "P": 0, "K": 0, "pH": (6.5, 8.0)},
    #     "laterite":{"N": 0, "P": 0, "K": 0, "pH": (5.5, 6.5)},
    #     "red": {"N": 0, "P": 0, "K": 0, "pH": (6.5, 7.5)},
    #     "black": {"N": 0, "P": 0, "K": 0, "pH": (6.5, 7.5)},
    #     "mountain": {"N": 0, "P": 0, "K": 0, "pH": (6.5, 7.5)},
    #     "desert": {"N": 0, "P": 0, "K": 0, "pH": (7.5, 8.5)}
    # }

    return json.dumps({"soil": soils[locname[-3].strip()]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)