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
    angle = int(data['slider1']) #sets angle to be from json dump file
    act = data['action'] #sets act to be from json dump file
  S = Stepper(0x48) #initializes S to be a stepper class
  if data['action'] == 'rotate': #Runs if rotate button is pressed
    S.goAngle(angle) #rotates to given angle
    sleep(5) #sleeps 5 seconds
  if data['action'] == 'zero': #runs if zero button is pressed
    S.zero() #zeros angle
    angle = 0

#sends angle data to thingspeak
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

