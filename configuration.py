"""Configurations for the RC car"""

PICAMERA_RESOLUTION_WIDTH = 640
PICAMERA_RESOLUTION_HEIGHT = 480
PICAMERA_RESOLUTION = (PICAMERA_RESOLUTION_WIDTH, PICAMERA_RESOLUTION_HEIGHT)
PICAMERA_FRAMERATE = 10
PICAMERA_WARM_UP_TIME = 5
# 100 - 200 Daytime and 400 - 800 Nighttime 
PICAMERA_ISO = 800
PICAMERA_BRIGHTNESS = 50

BACK_MOTOR_DATA_ONE = 17
BACK_MOTOR_DATA_TWO = 27
BACK_MOTOR_ENABLE_PIN = 22
FRONT_MOTOR_DATA_ONE = 19
FRONT_MOTOR_DATA_TWO = 26
PWM_FREQUENCY = 1000
INITIAL_PWM_DUTY_CYCLE = 100

TMP_BUFFER_DIR = '/tmp/'
PI_HOST_PORT = ('192.168.0.187', 8080)
PC_HOST_PORT = ('192.168.0.193', 8090)