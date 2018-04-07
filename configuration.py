"""Configurations for the RC car"""

PICAMERA_RESOLUTION_WIDTH = 640
PICAMERA_RESOLUTION_HEIGHT = 480
PICAMERA_RESOLUTION = (PICAMERA_RESOLUTION_WIDTH, PICAMERA_RESOLUTION_HEIGHT)
PICAMERA_FRAMERATE = 60
PICAMERA_WARM_UP_TIME = 2
# 100 - 200 Daytime and 400 - 800 Nighttime 
PICAMERA_ISO = 800
PICAMERA_BRIGHTNESS = 60

BACK_MOTOR_DATA_ONE = 17
BACK_MOTOR_DATA_TWO = 27
BACK_MOTOR_ENABLE_PIN = 22
FRONT_MOTOR_DATA_ONE = 19
FRONT_MOTOR_DATA_TWO = 26
PWM_FREQUENCY = 1000
INITIAL_PWM_DUTY_CYCLE = 100

CLASSIFICATION_LABELS = ['up', 'down', 'left', 'right', 'idle']
CLASSIFICATION_LABELS_AND_VALUES = {
    'up': [1, 0, 0, 0, 0],
    'down': [0, 1, 0, 0, 0],
    'left': [0, 0, 1, 0, 0],
    'right': [0, 0, 0, 1, 0],
    'idle': [0, 0, 0, 0, 1]
}


IMAGE_DIMENSIONS = (75, 75)
LAMBDA = 0.0
HIDDEN_LAYER_SIZE = 50
