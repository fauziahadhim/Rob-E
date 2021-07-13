# This is ACTIVE - Morning task
# If this isn't the script
# that you intend to run,
# please refresh/reload the app.
# Note: Put Rob-E on the floor to move.

import sys
sys.path.append(r'/opt/ezblock')
from ezblock import delay
from ezblock import TTS
from ezblock import Pin
from ezblock import Ultrasonic
from ezblock import mapping
from ezblock import delay
from ezblock import print
from picarmini import forward
from picarmini import backward
from picarmini import stop
from picarmini import set_dir_servo_angle
from picarmini import dir_servo_angle_calibration
from Music import *
from itertools import count
from multiprocessing import Process
import time
import random


news = None
Ref1 = None
distance = None
Ref2 = None
talk = None
musicNroam = None
musicNdance = None
__tts__ = TTS()

Ref1 = 30
Ref2 = 10

news = ''


thought = ''

dir_servo_angle_calibration(0)
pin_D0=Pin("D0")
pin_D1=Pin("D1")

music_set_volume(80)
__tts__.say('Good morning! This is Active Morning task.')
print('Active - Morning')
time.sleep(2)
print('Rob-E is telling you the news.')
__tts__.say(news)
time.sleep(2)


def movement():
  global Ref1, distance, Ref2
  while True:
    distance = Ultrasonic(pin_D0, pin_D1).read()
    if distance >= Ref1:
      set_dir_servo_angle(0)
      forward(15)
    elif distance >= Ref2:
      set_dir_servo_angle(40)
      forward(5)
      delay(500)
    else:
      set_dir_servo_angle((-40))
      backward(30)
      delay(500)

def roaming():
  p1 = Process(target = movement)
  p1.start()
  p1.join(timeout = 600)
  p1.terminate()
  stop()
  music_stop()
  
def music_and_roam():
  __tts__.say('What do you think about some music?')
  music_set_volume(80)
  background_music('act_morning_01.mp3')
  musicNroam = roaming()
  

def dance():
  while True:
    set_dir_servo_angle((-30))
    delay(500)
    set_dir_servo_angle(30)
    delay(500)
    set_dir_servo_angle(0)
    delay(500)
    forward(20)
    delay(100)
    backward(20)
    delay(100)
    stop()
    set_dir_servo_angle((-30))
    delay(500)
    set_dir_servo_angle(30)
    delay(500)
    set_dir_servo_angle(0)
    delay(500)
    forward(10)
    delay(200)
    backward(10)
    delay(200)
    forward(10)
    delay(200)
    backward(10)
    delay(200)
    forward(10)
    delay(200)
    backward(10)
    delay(200)
    stop()
    set_dir_servo_angle(0)
    
def dancing():
  p2 = Process(target = dance)
  p2.start()
  p2.join(timeout = 600)
  p2.terminate()
  stop()
  music_stop()
  
def music_and_dance():
  __tts__.say('I feel like dancing! Woohoo')
  music_set_volume(100)
  background_music('dragostea.mp3')
  musicNdance = dancing()


def talking():
  print('Rob-E is telling you his thoughts.')
  music_set_volume(80)
  __tts__.say(thought)
  time.sleep(2)
  __tts__.say('Anyway!')


def forever():
  __tts__.say('I am tired! I want to go back')
  time.sleep(1)


random_choices = [music_and_dance, music_and_roam, talking]
routine = random.choice(random_choices)()
stop()
music_stop()
music_set_volume(80)

