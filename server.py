from flask import Flask
import requests, json, time
from flask_cors import CORS, cross_origin
import mraa

url = "https://api.darksky.net/forecast/d19642947c22791bf57113f02837e88f/40.9257,-73.1409"



app = Flask(__name__)
CORS(app)

@app.route('/current')
def current_weather():
    """Returns the current weather in Stony Brook"""
    payload = {
        'exclude': 'flags,minutely,hourly,daily',
    }

    response = requests.get(url, params=payload)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys=True))
    return json.dumps(response, indent=4, sort_keys=True)

@app.route('/forecast')
def forecast():
    """Gives the forward weather forcast"""
    payload = {
        'exclude': 'flags,minutely,currently',
    }

    response = requests.get(url, params=payload)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys=True))
    return json.dumps(response, indent=4, sort_keys=True)

@app.route('/history/<int:days_back>')
def history(days_back):
    """Gives back weather history from days_back days back"""

    payload = {
        'exclude': 'flags,minutely,hourly,currently',
    }
    print(url + ',' + str(int(time.time()) - 86400))
    response = requests.get(url + ',' + str(int(time.time()) - (86400 * days_back)), params=payload)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys=True))
    return json.dumps(response, indent=4, sort_keys=True)


@app.route('/water/<float:valve_time>')
def water_endpoint(valve_time):
    """The endpoint which allows a user to force water the plant from their browser"""
    water(valve_time)
    return 'watered'

def water(valve_time):
    """This function is responsible for opening the solenoid valve for the set amount of time"""

    valve = mraa.Gpio(12)
    valve.dir(mraa.DIR_OUT)
    valve.write(1)
    time.sleep(valve_time)
    valve.write(0)

@app.route('/moisture')
def current_moisture():
    return str(float(measure_moisture()))


def measure_moisture():
    """Each of the sensors is calibrated for a specific soil moisture level. If the moisture level is present, the sensor
         output bit will flip from 0 to 1.We read each one, and assign the moisture level based on the sum"""

    sensor7 = mraa.Gpio(7)
    sensor7.dir(mraa.DIR_IN)

    sensor6 = mraa.Gpio(6)
    sensor6.dir(mraa.DIR_IN)

    sensor5 = mraa.Gpio(5)
    sensor5.dir(mraa.DIR_IN)

    sensor4 = mraa.Gpio(4)
    sensor4.dir(mraa.DIR_IN)
    print(float(sensor7.read() + sensor6.read() + sensor5.read() + sensor4.read()))
    return float(sensor7.read() + sensor6.read() + sensor5.read() + sensor4.read())