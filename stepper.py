
from PCF8591 import PCF8591 #imports PCF8591 class
import RPi.GPIO as GPIO
import time

import smbus
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

pins = [18,21,22,23] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

# Define the pin sequence for counter-clockwise motion, noting that
# two adjacent phases must be actuated together before stepping to
# a new phase so that the rotor is pulled in the right direction:
sequence = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]

state = 0 #current position of stator sequence 

def delay_us(tus): # use microseconds to improve time resolution
  endTime = time.time() + float(tus)/ float(1E6)
  while time.time() < endTime:
    pass
    
class Stepper:
  currentangle = 0
  def __init__(self, address): #instantiates address 
    self.adc = PCF8591(address) #calls PCF8591 class by composition
  def __halfstep(self,dir):#creates private halfstep method
    global state 
    state += dir
    if state > 7: state = 0
    elif state < 0: state = 7
    for pin in range(4):
      GPIO.output(pins[pin], sequence[state][pin])
    delay_us(1000)
  def __moveSteps(self,steps, dir): #creates private movesteps method
    for step in range(steps):
      self.__halfstep(dir)
  def goAngle(self, angle): #creates go angle method
    x = abs(angle - Stepper.currentangle) % 360 #sets x to be difference of currentangle and angle
    if Stepper.currentangle != angle: #runs if angle is not equal to current angle
      if abs(angle - Stepper.currentangle) > 180: #runs if difference is greater than 180
        l = 360 - x #sets l to be 360 - x
      else: #runs if difference less than 180
        l = x 
      step = int(((l)/360)*512*8) #sets step based on l
      if x < 180: #runs if x is less than 180
        if angle > Stepper.currentangle: #runs if angle greater than current angle
          self.__moveSteps(step,1)
          Stepper.currentangle = angle
        if angle < Stepper.currentangle: #runs if angle less than current angle
          self.__moveSteps(step,-1)
          Stepper.currentangle = angle
      if x > 180: 
        if angle < Stepper.currentangle: #runs if angle less than current angle
          self.__moveSteps(step,1)
          Stepper.currentangle = angle
        if angle > Stepper.currentangle: #runs if angle greater than current angle
          self.__moveSteps(step,-1)
          Stepper.currentangle = angle
  def zero(self): #creates zero method
    GPIO.output(27, 1) #sets pin 27 to be high
    sleep(.5)
    while self.adc.read(0) < 160: #runs while photoresistor can see led
      GPIO.output(27, 1) #sets pin 27 to be high
      self.__moveSteps(20,1) #moves 20 steps
    GPIO.output(27, 0) #sets pin 27 to be low
    sleep(1)
    Stepper.currentangle = 0 #sets current angle to be 0
