
#from PCF8591 import PCF8591 #imports PCF8591 class
import RPi.GPIO as GPIO
import time

import smbus
from time import sleep

class PCF8591:

  def __init__(self,address):
    self.bus = smbus.SMBus(1)
    self.address = address

  def read(self,chn): #channel
      try:
          self.bus.write_byte(self.address, 0x40 | chn)  # 01000000
          self.bus.read_byte(self.address) # dummy read to start conversion
      except Exception as e:
          print ("Address: %s \n%s" % (self.address,e))
      return self.bus.read_byte(self.address)

  def write(self,val):
      try:
          self.bus.write_byte_data(self.address, 0x40, int(val))
      except Exception as e:
          print ("Error: Device address: 0x%2X \n%s" % (self.address,e))

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
  def goAngle(self, angle):
    step = int(((angle-Stepper.currentangle)/360)*512*4)
    if Stepper.currentangle != angle:
      if angle <= 180:
        moveSteps(step,1)
        Stepper.currentangle += angle
      if (angle > 180) and (angle < 360):
        moveSteps((step-512*4)*-1,-1)
        Stepper.currentangle += angle
  #def zero(self):
   # GPIO.output(27, 1)
   # while self.adc.read(0) > 100: #check to see what normal value is
      moveSteps(20,1)
    GPIO.output(27, 0)
    
  
'''
class Stepper:
  def __init__(self, angle):
    self.angle = angle
    #self.adc = PCF8591(address)
  def goAngle(self, angle):
    step = int((self.angle/360)*512*4)
    if self.angle <= 180:
      moveSteps(step,1)
    if (self.angle > 180) and (self.angle < 360):
      moveSteps((step-512*4)*-1,-1)
  def zero(self):
    GPIO.output(27, 1)
    while self.adc.read(0) > 100: #check to see what normal value is
      moveSteps(20,1)
    GPIO.output(27, 0)
    self.angle = 0
    #currentstep = 0

S = Stepper(200)
#moveSteps(512*4,1)
S.goAngle(200) 
GPIO.setup(16, GPIO.OUT)
pwm = GPIO.PWM(16, 1) # PWM object on our pin at 100 Hz
pwm.start(75)
sleep(2)
GPIO.cleanup() 
'''