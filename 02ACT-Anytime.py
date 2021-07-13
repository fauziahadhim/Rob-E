# This is ACTIVE - Anytime task
# If this isn't the script
# that you intend to run,
# please refresh/reload the app.
# Put Rob-E on the floor to roam.
# Camera stream is available.

from vilib import Vilib
from ezblock import delay
from ezblock import TTS
from picarmini import forward
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
from picarmini import camera_servo1_angle_calibration
from picarmini import camera_servo2_angle_calibration
from picarmini import set_camera_servo2_angle
from picarmini import dir_servo_angle_calibration
from Music import *
from ezblock import WiFi
import time
import random
from multiprocessing import Process


__tts__ = TTS()
Ref1 = None
distance = None
Ref2 = None
funfact = None

funfact1 = ''
funfact2 = ''
funfact3 = ''
funfact4 = ''
funfact5 = ''

Ref1 = 30
Ref2 = 10


def move():
  while Vilib.human_detect_object(('number')) == 0:
    camera_servo1_angle_calibration(20)
    camera_servo2_angle_calibration(30)
    time.sleep(3)
    camera_servo1_angle_calibration(-20)
    camera_servo2_angle_calibration(30)
    time.sleep(3)
    camera_servo1_angle_calibration(0)
    camera_servo2_angle_calibration(30)
    time.sleep(3)
    camera_servo1_angle_calibration(20)
    camera_servo2_angle_calibration(25)
    time.sleep(3)
    camera_servo1_angle_calibration(-20)
    camera_servo2_angle_calibration(25)
    time.sleep(3)
    camera_servo1_angle_calibration(0)
    camera_servo2_angle_calibration(25)
    time.sleep(3)


def forever():
  global Ref1, distance, Ref2, funfact, move
  distance = Ultrasonic(pin_D0, pin_D1).read()
  if (Vilib.human_detect_object(('number'))) == 1:
    p1.terminate()
    stop()
    camera_servo1_angle_calibration(0)
    camera_servo2_angle_calibration(30)
    music_set_volume(80)
    __tts__.say('Hello there! Aw are you alone again?')
    print('There is 1 person detected.')
    print('Rob-E plays music.')
    music_set_volume(100)
    background_music('titanic.mp3')
    time.sleep(108)
    music_stop()
    p1.start()
  if (Vilib.human_detect_object(('number'))) == 2:
    p1.terminate()
    stop()
    camera_servo1_angle_calibration(0)
    camera_servo2_angle_calibration(30)
    print('There are 2 people detected.')
    music_set_volume(80)
    __tts__.say('Hello there!')
    funfact = random.choice(random_facts)
    print('Funfact: ' + funfact)
    music_set_volume(80)
    __tts__.say('Did you know that')
    __tts__.say(funfact)
    p1.start()
  if (Vilib.human_detect_object(('number'))) == 5:
    p1.terminate()
    stop()
    camera_servo1_angle_calibration(0)
    camera_servo2_angle_calibration(30)
    print('There are 5 people detected!')
    music_set_volume(80)
    __tts__.say('Corona party! Corona party!')
    sound_effect_play('Emergency_Police.wav',100)
    time.sleep(120)
    music_stop()
    p1.start()
  if distance >= Ref1:
    set_dir_servo_angle(0)
    forward(15)
  elif distance >= Ref2:
    set_dir_servo_angle(40)
    forward(5)
    delay(200)
  else:
    set_dir_servo_angle((-40))
    backward(30)
    delay(200)


Vilib.camera_start(True)
Vilib.human_detect_switch(True)
dir_servo_angle_calibration(0)
camera_servo1_angle_calibration(0)
camera_servo2_angle_calibration(25)
WiFi().write('GB', 'ssid', 'psk')
pin_D0 = Pin("D0")
pin_D1 = Pin("D1")
print('Active - Anytime')
music_set_volume(80)
__tts__.say('Moin! This is Active Anytime task!')
random_facts = [funfact1, funfact2, funfact3, funfact4, funfact5]
p1 = Process(target = move)
p1.start()

