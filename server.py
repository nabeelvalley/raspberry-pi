from picamera import PiCamera

import io
from threading import Condition
from flask import Response

from camera.stream import as_http_response, gen

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera/feed')
def camera_feed():
    return as_http_response()

@app.route('/camera/predict')
def camera_predict():
    return "Jello"

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)