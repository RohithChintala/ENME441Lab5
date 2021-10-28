#!/usr/bin/python37all

from stepper import Stepper
import RPi.GPIO as GPIO 
import json
from time import sleep
from urllib.request import urlopen
from urllib.parse import urlencode

while True: #runs continuously
  with open('led-pwm.txt', 'r') as f: #opens json dump file
    data = json.load(f) #sets data to be loaded from json dump file
    angle = int(data['slider1'])
    act = data['action']
  S = Stepper()
  S.goAngle(angle)
  sleep(2)
  #if data['action'] == 'r':
  #if data['action'] == 'z':
  #  S.zero()
'''
  api = "QYSPJIYIF0S3QIEU"   #####CORRECT FOR MY API
  params = {
    "api_key":api,
    1: s1}
  params = urlencode(params)   # put dict data into a GET string

  # add "?" to URL and append with parameters in GET string:
  url = "https://api.thingspeak.com/update?" + params
  try:
    response = urlopen(url)      # open the URL to send the request
    print(response.status, response.reason)  # display the response
    print(response.read()) # display response page data
    time.sleep(16)    # 15 sec minimum
  except Exception as e:
    print(e)
'''
