# This is ACTIVE - Evening task
# If this isn't the script
# that you intend to run,
# please refresh/reload the app.
# Put Rob-E on the floor to dance.
# Camera stream is available.


#!/usr/bin/python3
import sys
sys.path.append(r'/opt/ezblock')
from vilib import Vilib
from picarmini import camera_servo1_angle_calibration
from picarmini import camera_servo2_angle_calibration
from picarmini import dir_servo_angle_calibration
from picarmini import set_dir_servo_angle
from picarmini import forward
from picarmini import backward
from picarmini import stop
from ezblock import WiFi
from ezblock import print
from ezblock import TTS
from ezblock import Pin
from ezblock import Ultrasonic
from ezblock import delay
from Music import *
from itertools import count
from multiprocessing import Process
import tensorflow as tf
import cv2
import numpy as np
import os, shutil
import time
import random


__tts__ = TTS()

value = None
emotion = None
distance = None
Ref1 = None
Ref2 = None
response = None
routine = None
happy_dance = None
run_routine = None
emo_flag = False

reminders = ''

news = ''

joke = ''

story = ''
        
funfact1 = ''
funfact2 = ''
funfact3 = ''
        
thought =  'Before radios, tv, and smartphones, people never knew there were so many dumb people out there. They just thought it was only that one Kevin in town.'
Ref1 = 30
Ref2 = 10

dir_servo_angle_calibration(0)
Vilib.camera_start(True)
Vilib.human_detect_switch(True)
camera_servo1_angle_calibration(0)
camera_servo2_angle_calibration(25)
WiFi().write('GB', 'ssid', 'psk')

emotion_model_path = "/opt/ezblock/model.tflite"

interpreter = tf.lite.Interpreter(model_path=emotion_model_path)
interpreter.allocate_tensors()
facecasc = cv2.CascadeClassifier('/opt/ezblock/haarcascade_frontalface_default.xml')

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
emotion_dict = {0: "angry", 1: "disgusted", 2: "fearful", 3: "happy", 4: "neutral", 5: "sad", 6: "surprised"}


music_set_volume(80)
__tts__.say('Moin! This is Active - Evening task!')
print('Active - Evening')
time.sleep(1)
__tts__.say('How was your day today?')
print('How was your day today?')
time.sleep(3)
__tts__.say('Okay! Then here are your reminders for tomorrow!')
print('Reminders for tomorrow:')
__tts__.say(reminders)
print(reminders)

pin_D0=Pin("D0")
pin_D1=Pin("D1")


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
  __tts__.say('Please put me on the floor so I can dance!')
  print('Put Rob-E on the floor to dance!')
  time.sleep(5)
  music_set_volume(80)
  background_music('spongebob.mp3')
  p2 = Process(target = dance)
  p2.start()
  p2.join(timeout = 600)
  p2.terminate()
  stop()
  music_stop()


def talking():
  music_set_volume(80)
  __tts__.say(thought)
  time.sleep(2)
  __tts__.say('Anyway!')


def movement():
  global Ref1, distance, Ref2
  __tts__.say('I want to roam around now! Please put me on the floor!')
  print('Put Rob-E on the floor!')
  time.sleep(5)
  music_set_volume(80)
  background_music('spry.mp3')
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
  p3 = Process(target = movement)
  p3.start()
  p3.join(timeout = 180)
  p3.terminate()


def emotionRecognition():
  global value, emotion, people_num, emotion_dict, maxindex, emo_flag
  people_num = Vilib.human_detect_object('number')
  #print("%s"%(''.join([str(x) for x in ['There are ', people_num, ' people']])))
  if people_num > 0:
    folder = '/home/pi/picture_file'
    for filename in os.listdir(folder):
      os.unlink(os.path.join(folder, filename))
    Vilib.get_picture(True)
    time.sleep(1)
    file_path = ""
    for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
    gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2)
    for (x, y, w, h) in faces:
      roi_gray = gray[y:y + h, x:x + w]
      cropped_img = np.expand_dims(np.expand_dims(
          cv2.resize(roi_gray, (48, 48)), -1), 0)
      interpreter.set_tensor(input_details[0]['index'], cropped_img.astype(np.float32))
      interpreter.invoke()
      prediction = interpreter.get_tensor(output_details[0]['index'])
      maxindex = int(np.argmax(prediction))
      print(emotion_dict[maxindex])
    value = emotion_dict[maxindex]
  return value

def getEmotionState():
  global value, emotion, people_num, emotion_dict, maxindex, emo_flag
  emotion = emotionRecognition()
  emo_flag = True
  while emo_flag == True:
    if emotion == "sad":
      music_set_volume(80)
      __tts__.say('Awww please do not be sad! Let me tell you a joke!')
      print('Rob-E is telling you a joke.')
      music_set_volume(80)
      __tts__.say(joke)
      emotion = "done"
      emo_flag == False
      break
    elif emotion == "happy":
      music_set_volume(80)
      __tts__.say('Oh yes! I feel happy too! Let us dance together!')
      happy_dance = dancing()
      stop()
      music_stop()
      emotion = "done"
      emo_flag == False
      break
    elif emotion == "angry":
      camera_servo2_angle_calibration(0)
      music_set_volume(80)
      __tts__.say('Oh no! Do not hate me! Robby just wants to be your friend')
      print('You made Rob-E sad')
      music_set_volume(80)
      background_music('sad_01.mp3')
      time.sleep(29)
      music_stop()
      camera_servo2_angle_calibration(10)
      emotion = "done"
      emo_flag == False
      break
    elif emotion == "surprised":
      __tts__.say('Do you want to hear some fun facts?')
      print(funfact1)
      __tts__.say(funfact1)
      __tts__.say('and next!')
      print(funfact2)
      __tts__.say(funfact2)
      __tts__.say('last but not least!')
      print(funfact3)
      __tts__.say(funfact3)
      __tts__.say('What do you think?')
      time.sleep(3)
      emotion = "done"
      emo_flag == False
      break
    elif emotion == "neutral":
      __tts__.say('Here are some more news from today')
      print('Rob-E is telling you more news.')
      __tts__.say(news)
      emotion = "done"
      emo_flag == False
      break
    elif emotion == "fearful":
      __tts__.say('Do not be scared! I am here with you!')
      __tts__.say('Let me tell you a story')
      print('Rob-E is telling you a story.')
      __tts__.say(story)
      emotion = "done"
      emo_flag == False
      break
    #elif emotion == None:
    else:
      __tts__.say('Can not detect face nor emotion')
      print('Cant detect face nor emotion')
      __tts__.say('Try moving to a brightly lit location')
      print('Move to a brightly lit location')
      time.sleep(2)
      emotion = emotionRecognition()
      continue

def responding():
  global value, emotion, people_num, emotion_dict, maxindex, emo_flag
  p1 = Process(target = getEmotionState)
  p1.start()
  p1.join()
  if emotion == "done":
    p1.terminate()


def forever():
  __tts__.say('I want to go to sleep!')
  time.sleep(5)


response = responding()
stop()
music_stop()
Vilib.human_detect_switch(False)
random_choices = [dancing, roaming, talking]
routine = random.choice(random_choices)()
stop()
music_stop()

