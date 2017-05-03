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

@app.route('/history/<days_back>')
def history(days_back):
    payload = {
        'exclude': 'flags,minutely,hourly,currently',
    }
    print(url + ',' + str(int(time.time()) - 86400))
    response = requests.get(url + ',' + str(int(time.time()) - (86400 * days_back)), params=payload)
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

@app.route('/moisture')
def current_moisture():
    sensor7 = mraa.Gpio(7)
    sensor7.dir(mraa.DIR_IN)
    print(sensor7.read())

    sensor6 = mraa.Gpio(6)
    sensor6.dir(mraa.DIR_IN)
    print(sensor6.read())

    sensor5 = mraa.Gpio(5)
    sensor5.dir(mraa.DIR_IN)
    print(sensor5.read())

    sensor4 = mraa.Gpio(4)
    sensor4.dir(mraa.DIR_IN)
    print(sensor4.read())
    return str(float(sensor7.read() + sensor6.read() + sensor5.read() + sensor4.read()))
