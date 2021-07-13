# This is PASSIVE - Anytime task
# If this isn't the script
# that you intend to run,
# please refresh/reload the app.


from vilib import Vilib
from ezblock import print
from ezblock import Remote
from ezblock import WiFi
from picarmini import forward
from ezblock import mapping
from picarmini import set_dir_servo_angle
from picarmini import dir_servo_angle_calibration
from picarmini import camera_servo1_angle_calibration
from picarmini import camera_servo2_angle_calibration
from picarmini import set_camera_servo2_angle


__RM_OBJECT__ = Remote()

Vilib.camera_start(True)
dir_servo_angle_calibration(0)
camera_servo1_angle_calibration(0)
camera_servo2_angle_calibration(25)
WiFi().write('GB', 'ssid', 'psk')


def forever():
  __RM_OBJECT__.read()
  forward(__RM_OBJECT__.get_joystick_value("A", "Y"))
  set_dir_servo_angle((mapping(__RM_OBJECT__.get_joystick_value("A", "X"), (-100), 100, (-45), 45)))
