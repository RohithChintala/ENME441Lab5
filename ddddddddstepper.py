import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pins = [18,21,22,23] # controller inputs: in1, in2, in3, in4
for pin in pins:
  GPIO.setup(pin, GPIO.OUT, initial=0)

# Define the pin sequence for counter-clockwise motion, noting that
# two adjacent phases must be actuated together before stepping to
# a new phase so that the rotor is pulled in the right direction:
ccw = [ [1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
        [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
# Make a copy of the ccw sequence. This is needed since simply
# saying cw = ccw would point both variables to the same list object:
cw = ccw[:]  # use slicing to copy list (could also use ccw.copy() in Python 3)
cw.reverse() # reverse the new cw sequence

def delay_us(tus): # use microseconds to improve time resolution
  endTime = time.time() + float(tus)/ float(1E6)
  while time.time() < endTime:
    pass


def loop(dir, step): 
  for i in range(step): 
    for halfstep in range(8):
      for pin in range(4):    
        GPIO.output(pins[pin], dir[halfstep][pin])
      delay_us(1000) ###### SEE HOW FAST TO MAKE IT

class Stepper:
  def __init__(self, angle):
    self.angle = angle
  def goAngle(self, angle):
    step = (angle/360)*512
    if angle < 180:
      loop(cw, step)
     if angle > 180:
      loop(ccw, step)
  def zero(self):

try:
  loop(cw)
  loop(ccw)
except: KeyboardInterrupt: #ends code with keyboard interupt
 print('\nExiting')
GPIO.cleanup()