#!/usr/bin/python37all
from stepper import Stepper
import RPi.GPIO as GPIO 
import json
from time import sleep
from urllib.request import urlopen
from urllib.parse import urlencode

while True: #runs continuously
  with open('s.txt', 'r') as f: #opens json dump file
    data = json.load(f) #sets data to be loaded from json dump file
    angle = int(data['slider1'])
    act = data['action']
  S = Stepper(0x48)
  if data['action'] == 'rotate':
    S.goAngle(angle)
    sleep(5)
  if data['action'] == 'zero':
    S.zero()


  api = "QYSPJIYIF0S3QIEU"
  params = {
    "api_key":api,
    1: angle}
  params = urlencode(params)  

  url = "https://api.thingspeak.com/update?" + params
  try:
    response = urlopen(url)  
    print(response.status, response.reason) 
    print(response.read()) 
    time.sleep(16)
  except Exception as e:
    print(e)

