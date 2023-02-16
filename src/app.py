from __future__ import division, print_function
import sys
sys.path.append('../')

from flask import Flask, request, render_template
import json
import requests
import datetime
import pickle
import numpy as np
from funcs import location

app = Flask(__name__)

############

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf

import pathlib
import wget

from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#############

# GLOBALS: ########################################################################################
MODEL = None

LATITUDE = ''
LONGITUDE = ''
SOIL_TYPE = ''
SOIL_CATEGORY = ''
STATE = ''
PH = 0.0
TEMPERATURE = 0.0
PRECIPITATION = 0.0
HUMIDITY = 0.0
###################################################################################################

def get_soil(state):
    index = {
        ''
    }
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

    return soils[STATE], pH[STATE]



def get_weather():
    start_date = datetime.datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d')
    end_pt = f'https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m,relativehumidity_2m,precipitation&timezone=auto&start_date={start_date}&end_date={end_date}'
    return json.loads(requests.get(end_pt).text)
    


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')



@app.route('/get_loc/<string:loc>', methods=['POST'])
def get_loc(loc):
    global MODEL, LATITUDE, LONGITUDE, SOIL_TYPE, SOIL_CATEGORY, STATE, PH, TEMPERATURE, PRECIPITATION, HUMIDITY 
    MODEL = pickle.load(open('./machine-learning/model', 'rb'))
    locs = json.loads(loc)
    LATITUDE = locs['latitude']
    LONGITUDE = locs['longitude']
    STATE = location.get_location(LATITUDE, LONGITUDE)[-3].strip()
    weather = get_weather()

    def avg(num):
        num = [item for item in num if item != None and item != 0]
        sum_num = 0
        for t in num:
            sum_num = sum_num + t           
        avg = sum_num / (len(num)+1)
        return avg

    TEMPERATURE = weather['hourly']['temperature_2m']
    HUMIDITY = weather['hourly']['relativehumidity_2m']
    PRECIPITATION = weather['hourly']['precipitation']
    SOIL_TYPE, PH = get_soil(STATE)

    # print(LATITUDE, LONGITUDE, SOIL_TYPE, SOIL_CATEGORY, STATE, PH, avg(TEMPERATURE), avg(PRECIPITATION), avg(HUMIDITY), datetime.date.today().month)

    print(MODEL.predict([[PH, avg(TEMPERATURE), avg(PRECIPITATION), avg(HUMIDITY), datetime.date.today().month,
                                     0,
                                     1,
                                     0,
                                     0,
                                     0,
                                     1,
                                     0]]))

    return('/')


#########
MODEL_PATH = 'model_resnet.hdf5'
MODEL_URL = 'https://github.com/DARK-art108/Cotton-Leaf-Disease-Prediction/releases/download/v1.0/model_resnet.hdf5'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

# Download model if not present
while not pathlib.Path(MODEL_PATH).is_file():
    print(f'Model {MODEL_PATH} not found. Downloading...')
    wget.download(MODEL_URL)

# Define a flask app
app = Flask(__name__)

# Define upload path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Developing in the absence of TensorFlow :P (Python 3.9.0 x64)
# def load_model(aa):
#     class a:
#         @staticmethod
#         def predict(*args):
#             return 1
#     return a()

# class image:
#     @staticmethod
#     def load_img(path, target_size):
#         return 'a'

#     @staticmethod
#     def img_to_array(img):
#         return 'v'

# Load your trained model
model = load_model(MODEL_PATH)


def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x = x / 255
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x)

    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    if preds == 0:
        preds = "The leaf is a diseased cotton leaf."
    elif preds == 1:
        preds = "The leaf is a diseased cotton plant."
    elif preds == 2:
        preds = "The leaf is a fresh cotton leaf."
    else:
        preds = "The leaf is a fresh cotton plant."

    return preds


@app.route('/', methods=['GET', 'POST'])
def index():
    # Main page
    if request.method == 'POST':
        # Get the file from post request
        print(request.files, request.form, request.args)
        f = None
        if 'image' in request.files: f = request.files['image']
        if f:
            # Save the file to ./uploads
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(file_path)

            # Make prediction
            preds = model_predict(file_path, model)
            result = preds
            return render_template('cotton.html', result=result, img=secure_filename(f.filename))
        return render_template('cotton.html', result=None, err='Failed to receive file')
    # First time
    return render_template('cotton.html', result=None)

#########

@app.route('/dashboard/', methods=['GET'])
def dash():
    global TEMPERATURE, HUMIDITY
    print('habijabi')
    print(f'Values: {TEMPERATURE},{HUMIDITY}')
    return render_template('dashboard.html', temperature=TEMPERATURE, humidity=HUMIDITY)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, ssl_context='adhoc')