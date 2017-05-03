from flask import Flask
import requests, json, time
from flask_cors import CORS, cross_origin
import mraa

url = "https://api.darksky.net/forecast/d19642947c22791bf57113f02837e88f/40.9257,-73.1409"



app = Flask(__name__)
CORS(app)

@app.route('/current')
def current_weather():
    payload = {
        'exclude': 'flags,minutely,hourly,daily',
    }

    response = requests.get(url, params=payload)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys=True))
    return json.dumps(response, indent=4, sort_keys=True)

@app.route('/forecast')
def forecast():
    payload = {
        'exclude': 'flags,minutely,hourly,currently',
    }

    response = requests.get(url, params=payload)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys=True))
    return json.dumps(response, indent=4, sort_keys=True)

@app.route('/water/<float:valve_time>')
def water(valve_time):
    valve = mraa.Gpio(12)
    valve.dir(mraa.DIR_OUT)
    valve.write(1)
    time.sleep(valve_time)
    valve.write(0)
    return 'watered'
