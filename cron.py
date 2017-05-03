from flask import Flask
import requests, json, time
from flask_cors import CORS, cross_origin
import mraa

url = "https://api.darksky.net/forecast/d19642947c22791bf57113f02837e88f/40.9257,-73.1409"

def measure_moisture():
    sensor7 = mraa.Gpio(7)
    sensor7.dir(mraa.DIR_IN)

    sensor6 = mraa.Gpio(6)
    sensor6.dir(mraa.DIR_IN)

    sensor5 = mraa.Gpio(5)
    sensor5.dir(mraa.DIR_IN)

    sensor4 = mraa.Gpio(4)
    sensor4.dir(mraa.DIR_IN)
    return float(sensor7.read() + sensor6.read() + sensor5.read() + sensor4.read())

def water(valve_time):
    valve = mraa.Gpio(12)
    valve.dir(mraa.DIR_OUT)
    valve.write(1)
    time.sleep(valve_time)
    valve.write(0)

def rain_check():
    duration = 1.0
    if measure_moisture() < 1:
        duration+=1
    if measure_moisture() < 2:
        duration+=.5

    payload = {
        'exclude': 'flags,minutely,hourly',
    }
    response = requests.get(url, params=payload)
    response = response.json()
    print(response['currently']['precipIntensity'])
    if measure_moisture() > 3:
        duration*=0
    water(duration)

rain_check()
