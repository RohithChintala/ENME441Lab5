import RPi.GPIO as GPIO
import time

import smbus
from time import sleep



GPIO.setmode(GPIO.BCM)
#GPIO.setup(27, GPIO.OUT)

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

def halfstep(dir):
  # dir = +/- 1 (ccw or cw)
  state += dir
  if state > 7: state = 0
  elif state < 0: state = 7
  for pin in range(4):
    GPIO.output(pins[pin], sequence[state][pin])
  delay_us(1000)

def moveSteps(steps, dir):
  #move the actuation sequence a given number of half steps 
  for step in steps:
    halfstep(dir)



# Make a full rotation of the output shaft:
def loop(dir): # dir = rotation direction (cw or ccw)
  for i in range(512): # full revolution (8 cycles/rotation * 64 gear ratio)
    for halfstep in range(8): # 8 half-steps per cycle
      for pin in range(4):    # 4 pins that need to be energized
        GPIO.output(pins[pin], dir[halfstep][pin])
      delay_us(1000)


class Stepper:
  def __init__(self, angle):
    self.angle = angle
    #self.adc = PCF8591(address)
  def goAngle(self, angle):
    step = (self.angle/360)*512
    if self.angle < 180:
      movestep(step,-1)
    if self.angle > 180:
      movestep(step,1)
  #def zero(self):
    #GPIO.output(27, 1)
    #while self.adc.read(0) > 100: #check to see what normal value is
    #  movestep(8,1)
    #GPIO.output(27, 0)
    #self.angle = 0
    #currentstep = 0

try:
  loop(cw)
  #loop(ccw)
  S = StepperMotor(0x48)
  movestep(1000,1)
  sleep(2) 
except:
  pass
GPIO.cleanup() 