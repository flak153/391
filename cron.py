from flask import Flask
import requests, json, time
from flask_cors import CORS, cross_origin
import mraa, schedule

url = "https://api.darksky.net/forecast/d19642947c22791bf57113f02837e88f/40.9257,-73.1409"

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
    return float(sensor7.read() + sensor6.read() + sensor5.read() + sensor4.read())

def water(valve_time):
    """This function is responsible for opening the solenoid valve for the set amount of time"""
    valve = mraa.Gpio(12)
    valve.dir(mraa.DIR_OUT)
    valve.write(1)
    time.sleep(valve_time)
    valve.write(0)

def rain_check():
    """This is the function that gets run by a cron job everyday, every 6 hours. """
    duration = 0
    if measure_moisture() < 1:  #This is for less than 10% soil moisture
        duration+=1
    if measure_moisture() < 2:  #This is for less than 20% soil moisture
        duration+=.5

    payload = {
        'exclude': 'flags,minutely,hourly',
    }
    response = requests.get(url, params=payload) #Gets weather information from Dark Sky
    response = response.json()

    if (response['currently']['temperature']) > 85: #Add extra water if the temperature is greater than 85
        duration += .5
    if (response['currently']['precipIntensity']) > .01: #If it's raining don't wantr the plants
        duration = 0
    if measure_moisture() > 3: #If soil moisture is 40% or greater then do not water plants
        duration = 0
    water(duration)

schedule.every(6).hour.do(rain_check())

while True:
    schedule.run_pending()
    time.sleep(5)
