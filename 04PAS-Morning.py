# This is PASSIVE - Morning task
# If this isn't the script
# that you intend to run,
# please refresh/reload the app.
# Put Rob-E on the path to drive.

from picarmini import dir_servo_angle_calibration
from picarmini import set_dir_servo_angle
from picarmini import forward
from picarmini import backward
from picarmini import stop
from ezblock import delay
from ezblock import ADC
from ezblock import TTS
from ezblock import mapping
from ezblock import print
from vilib import Vilib
from Music import *
import time

sta = None
value = None
direction = None
Ref = None
Left = None
Mid = None
Right = None
lastSta = None
currentSta = None
driving = None

news = ''

dir_servo_angle_calibration(0)
Ref = 950
__tts__ = TTS()

"""Describe this function...
"""
def getDirection():
  global sta, value, direction, Ref, Left, Mid, Right, lastSta, currentSta
  value = getGrayscaleValue()
  if value == [0, 1, 0] or value == [1, 1, 1]:
    direction = 'FORWERD'
  elif value == [1, 0, 0] or value == [1, 1, 0]:
    direction = 'RIGHT'
  elif value == [0, 0, 1] or value == [0, 1, 1]:
    direction = 'LEFT'
  elif value == [0, 0, 0]:
    direction = 'OUT'
  return direction


adc_A0=ADC("A0")

adc_A1=ADC("A1")

adc_A2=ADC("A2")


"""Describe this function...
"""
def getGrayscaleValue():
  global sta, value, direction, Ref, Left, Mid, Right, lastSta, currentSta
  if (adc_A0.read()) <= Ref:
    Left = 1
  else:
    Left = 0
  if (adc_A1.read()) <= Ref:
    Mid = 1
  else:
    Mid = 0
  if (adc_A2.read()) <= Ref:
    Right = 1
  else:
    Right = 0
  return [Left, Mid, Right]


def movement():
  global sta, value, direction, Ref, Left, Mid, Right, lastSta, currentSta
  while True:
    sta = getDirection()
    if sta != 'OUT':
      lastSta = sta
    if sta == 'FORWERD':
      set_dir_servo_angle(0)
      forward(10)
    elif sta == 'LEFT':
      set_dir_servo_angle(20)
      forward(10)
    elif sta == 'RIGHT':
      set_dir_servo_angle((-20))
      forward(10)
    elif sta == 'OUT':
      stop()
      break

def forever():
  __tts__.say('Do not forget to switch me off!')
  time.sleep(3)

__tts__.say('Hello! This is Passive Morning Task')
print('Passive - Morning')
print('Put Rob-E on the start point of the driving path.')
__tts__.say('Please put me at the starting point of my driving path')
__tts__.say('I will wait')
time.sleep(5)
driving = movement()
stop()
print('Rob-E is telling you the news.')
__tts__.say(news)
time.sleep(5)
print('Turn Rob-E around to drive back.')
__tts__.say('Please turn me around so I can drive back.')
__tts__.say('I will wait')
time.sleep(5)
driving = movement()
stop()