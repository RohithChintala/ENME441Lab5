
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

def halfstep(dir): # dir = +/- 1 (ccw or cw)
  global state 
  state += dir
  if state > 7: state = 0
  elif state < 0: state = 7
  for pin in range(4):
    GPIO.output(pins[pin], sequence[state][pin])
  delay_us(1000)

def moveSteps(steps, dir):
  for step in range(steps):
    halfstep(dir)



# Make a full rotation of the output shaft:
def loop(dir): # dir = rotation direction (cw or ccw)
  for i in range(512): # full revolution (8 cycles/rotation * 64 gear ratio)
    for halfstep in range(8): # 8 half-steps per cycle
      for pin in range(4):    # 4 pins that need to be energized
        GPIO.output(pins[pin], dir[halfstep][pin])
      delay_us(1000)


class Stepper:
  currentangle = 0
  def __init__(self, address): #instantiates address 
    self.adc = PCF8591(address) #calls PCF8591 class by composition
  def goAngle(self, angle):
    #step = int((abs(angle-Stepper.currentangle)/360)*512*8)
    x = abs(angle - Stepper.currentangle) % 360
    if Stepper.currentangle != angle:
      if abs(angle - Stepper.currentangle) > 180:
        l = 360 - x
      else:
        l = x 
      step = int(((l)/360)*512*8)
      if x < 180:
        if angle > Stepper.currentangle:
          moveSteps(step,1)
          Stepper.currentangle = angle
        if angle < Stepper.currentangle:
          moveSteps(step,-1)
          Stepper.currentangle = angle
      if x > 180: 
        if angle < Stepper.currentangle:
          moveSteps(step,1)
          Stepper.currentangle = angle
        if angle > Stepper.currentangle:
          moveSteps(step,-1)
          Stepper.currentangle = angle
  def zero(self):
    GPIO.output(27, 1)
    sleep(.5)
    while self.adc.read(0) < 180: #check to see what normal value
      GPIO.output(27, 1)
      moveSteps(20,1)
      print(self.adc.read(0))
    GPIO.output(27, 0)
    Stepper.currentangle = 0
    sleep(1)
    GPIO.cleanup() 
